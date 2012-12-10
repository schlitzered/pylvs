# -*- coding: utf8 -*-
"""this Software is released under the MIT License
Copyright (c) 2012 Stephan Schultchen
"""

"""
pylvs.py

small wrapper around ipvsadm for handling Linux Virtual Server Instances
"""

import re
import socket
import subprocess

IPVSADM = "ipvsadm"
METHODS = ('ipip', 'masq', 'route')
PROTOS = ('tcp', 'udp')
SCHEDULERS = ('rr', 'wrr', 'lc', 'wlc', 'lblc', 
              'lblcr', 'dh', 'sh', 'sed', 'nq')

def _chkip(ipaddr):
    """check if given service_addr is a valid ipv6, or ipv4 address
    """    
    if not "[" in ipaddr:
        try:
            socket.inet_pton(socket.AF_INET, ipaddr)
            return True
        except socket.error:
            return False 
    else:
        try:
            ipaddr = ipaddr.replace('[', '').replace("]", '')
            socket.inet_pton(socket.AF_INET6, ipaddr)
            return True
        except socket.error:
            return False

def _mthcmd(method):
    """helper function to get the right cmd arg for the method
    """
    if method not in METHODS:
        raise ValueError, "Invalid LoadBalancing Method: {0}".format(method)
    
    if method == "ipip":
        mthcmd = "-i"
    elif method == "masq":
        mthcmd = "-m"
    else:
        mthcmd = "-g"
    return mthcmd

def _prtcmd(proto):
    """helper function to get the right cmd arg for the proto
    """
    if proto not in PROTOS:
        raise ValueError, "Invalid protocol: {0}".format(proto)
    
    if proto == "udp":
        prtcmd = "-u"
    else:
        prtcmd = "-t"
    return prtcmd

def _rangechk(minval, maxval, candidate):
    """check if candidate is within given range
    
    all values have to be a integer, or should be convertable to an integer
    """
    if (int(minval) <= int(candidate) and int(candidate) <= int(maxval)):
        return True
    else:
        return False

def validatereal_server(service_addr, real_server, method="masq"):
    """validate that real_server is correct for given service_addr 
    and loadbalancing method
    """
    
    ipsa, portsa = service_addr.rsplit(':', 1)
    iprs, portrs = real_server.rsplit(':', 1)
    
    #check that service and realserver use the same IP Version
    if (ipsa.startswith("[") and not iprs.startswith('[')):
        raise ValueError("IPv4 RealServer not allowed with "
                         "IPv6 Service")
    if (iprs.startswith("[") and not ipsa.startswith('[')):
        raise ValueError("IPv6 RealServer not allowed with "
                         "IPv4 Service")
    
    #only masquerading realservers are allowed to have different ports
    if method != "masq":
        if portsa != portrs:
            raise ValueError, "service_addr and RealServer port do not match, "\
        "this is a must for the non Masquerading RealServers"
    
    #service_addr & realserver address should not be the same
    if ipsa == iprs:
        raise ValueError, "service_addr & RealServer are the same, "\
    "this is not allowed"
    
    #validate realserver ip address
    if not _chkip(iprs):
        raise ValueError("invalid ip specified")
    
    #if we made it this far, everything is ok
    return True
    

def validateservice_addr(service_addr):
    """validate that service_addr is valid
    """
        
    ipsa, portsa = service_addr.rsplit(':', 1)
    
    if not _chkip(ipsa):
        raise ValueError("invalid ip specified")
    if not _rangechk(0, 65535, portsa):
        raise ValueError("port outside range")
    return True
    

class LVSInstance():
    """represents an Instance of a loadbalanced Service 
    """
    
    regex_mask = re.compile(".*-M (\S{1,})")
    regex_pers = re.compile(".*-p (\S{1,})")
    regex_sched = re.compile(".*-s (rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq).*")
    regex_rs = re.compile(".*-r (\S{1,}) (-(g|i|m)) -w (\S{1,})")
    
    def __init__(self, service_addr, proto):
        """manage an existing LVS instance 
        
        service_addr: ip:port
        proto: udp or tcp
        
        """
        self.service_addr = service_addr
        self.proto = proto
        self.prtcmd = _prtcmd(proto)
        
    def __str__(self):
        """set name of this object
        """
        return self.proto+"_"+self.service_addr
    
    def __repr__(self):
        """set name of this object
        """
        return self.proto+"_"+self.service_addr
    
    def __eq__(self, other):
        """make tests for the name of this object work
        """
        if self.__str__() == other:
            return True
        else:
            return False
        
    def __ne__(self, other):
        """make tests for the name of this object work
        """
        if self.__str__() == other:
            return False
        else:
            return True

    def add_server(self, real_server, method, **kwargs):
        """add new RealServer
        
        real_server: ip:port of RealServer
        method: which forwarding method (ipip, masq, route)
        
        optional arguments:
        weight: weight
        upper: upper threshold 
        lower: lover threshold, cannot appear without upper
        """
        
        #check if RealServer matches our service_addr
        validatereal_server(self.service_addr, real_server, method)
        
        cmd = [IPVSADM, "-a", self.prtcmd, self.service_addr, 
               "-r", real_server, _mthcmd(method)]
        
        # check for optional arguments & add them to the base command
        if 'weight' in kwargs:
            if _rangechk(0, 65535, kwargs['weight']):
                cmd = cmd + ['-w', str(kwargs['weight'])]
            else:
                raise ValueError("weight outside of valid range, "
            "should be within 1 and 65535, was {0}".format(kwargs['weight']))
        
        if 'upper' in kwargs:
            if _rangechk(1, 65535, kwargs['upper']):
                cmd = cmd + ['-x', str(kwargs['upper'])]
            else:
                raise ValueError("upper threshold outside of valid range, "\
                "should be within 1 and 65535, was {0}".format(kwargs['upper']))
        
        if 'lower' in kwargs:
            if not 'upper' in kwargs:
                raise ValueError("lower cannot appear without upper")
            
            if _rangechk(1, 65535, kwargs['lower']):
                cmd = cmd + ['-y', str(kwargs['lower'])]
            else:
                raise ValueError("lower threshold outside of valid range, "
            "should be within 1 and 65535, was {0}".format(kwargs['lower']))
        
        #lets try to add this RealServer
        try:
            subprocess.check_call(cmd)
            return True
        except:
            raise ValueError("could not add RealServer to service_addr, "
                             "probably already added?")
        
        
    def del_server(self, real_server):
        """remove RealServer
        
        real_server: ip:port of RealServer to remove
        """
        
        #check if realserver matches our service_addr
        validatereal_server(self.service_addr, real_server)
        
        cmd = [IPVSADM, "-d", self.prtcmd, self.service_addr, "-r", real_server]
        
        #lets try to remove this RealServer
        try:
            subprocess.check_call(cmd)
            return True
        except:
            raise ValueError("could not remove RealServer from service_addr, "
                             "probably already removed?")
        
    def edit_server(self, real_server, method, **kwargs):
        """add new RealServer
        
        real_server: ip:port of RealServer
        method: which forwarding method (ipip, masq, route)
        
        optional arguments:
        weight: weight
        upper: upper threshold 
        lower: lover threshold
        """
        
        #check if RealServer matches our service_addr        
        validatereal_server(self.service_addr, real_server, method)
        
        cmd = [IPVSADM, "-e", self.prtcmd, self.service_addr,
               "-r", real_server, _mthcmd(method)]
        
        # check for optional arguments & add them to the base command
        if 'weight' in kwargs:
            if _rangechk(0, 65535, kwargs['weight']):
                cmd = cmd + ['-w', str(kwargs['weight'])]
            else:
                raise ValueError("weight outside of valid range, "
            "should be within 1 and 65535, was {0}".format(kwargs['weight']))
        
        if 'upper' in kwargs:
            if _rangechk(1, 65535, kwargs['upper']):
                cmd = cmd + ['-x', str(kwargs['upper'])]
            else:
                raise ValueError("upper threshold outside of valid range, "
            "should be within 1 and 65535, was {0}".format(kwargs['upper']))
        
        if 'lower' in kwargs:
            if not 'upper' in kwargs:
                raise ValueError("lower cannot appear without upper")
            
            if _rangechk(1, 65535, kwargs['lower']):
                cmd = cmd + ['-y', str(kwargs['lower'])]
            else:
                raise ValueError("lower threshold outside of valid range, "
            "should be within 1 and 65535, was {0}".format(kwargs['lower']))
        
        #lets try to add this RealServer

        try:
            subprocess.check_call(cmd)
            return True
        except:
            raise ValueError("could not edit RealServer for this service_addr, "
                             "probably not added?")
        
    def list_servers(self):
        """ return a list with of tuples containing RealServers, 
        balancing method, and weight associated with this Service
        """
        
        cmd = subprocess.Popen([IPVSADM, "-Sn"], stdout=subprocess.PIPE)
        out, err = cmd.communicate()

        if err:
            raise ValueError("something has failed: {0}".format(err))
        candidates = out.split("\n")
        
        result = []
        
        for candidate in candidates:
            if candidate.startswith("-a "+self.prtcmd+" "+self.service_addr+
                                    " -r "):
                match = self.regex_rs.match(candidate)
                real_server = match.group(1)
                proto = match.group(2)
                if proto == "-m":
                    proto = "masq"
                elif proto == "-g":
                    proto = "route"
                else:
                    proto = "ipip"
                weight = match.group(4)
                result.append((real_server, proto, weight))
        return result
            
    def set_opts(self, scheduler, **kwargs):
        """set options for a service_addr
        
        scheduler: which scheduler to use
        
        optional args:
        persistence:
        netmask:
        """
        if scheduler in SCHEDULERS:
            cmd = [IPVSADM, "-E", self.prtcmd, self.service_addr, 
                   "-s", scheduler]
        else:
            raise ValueError("selected scheduler is invalid")
        
        if "persistence" in kwargs:
            if _rangechk(1, 65535, kwargs["persistence"]):
                cmd = cmd + ['-p', str(kwargs["persistence"])]
            else:
                raise ValueError("persistence outside of valid range, should "
            "be within 1 and 65535, was {0}".format(kwargs['persistence']))
        #FIXME: we should check that we have a valid netmask
        if "netmask" in kwargs:
            if not "persistence" in kwargs:
                raise ValueError("netmask cannot appear without persistence")
            cmd = cmd +["-M", kwargs["netmask"]]
        
        try:
            subprocess.check_call(cmd)
            return True
        except:
            raise ValueError("something went wrong")
                
    
    def get_opts(self):
        """get options for this service_addr
        
        will return a tuple like (scheduler, persistence, netmask)
        
        persistence and netmask are only returned if set
        """

        cmd = subprocess.Popen([IPVSADM, "-Sn"], stdout=subprocess.PIPE)
        out, err = cmd.communicate()
        
        if err:
            raise ValueError("something has failed: {0}".format(err))
        out = out.split("\n")
        
        for line in out:
            if line.startswith("-A "+self.prtcmd+" "+self.service_addr):
                scheduler = self.regex_sched.match(line).group(1)
                persistence = None
                netmask = None
                persistence = self.regex_pers.match(line)
                if persistence:
                    persistence = persistence.group(1)
                    netmask = self.regex_mask.match(line)
                    if netmask:
                        netmask = netmask.group(1)
                return (scheduler, persistence, netmask)
        
    def zero(self):
        """Zero the packet, byte and rate counters for this service_addr
        """
        try:
            subprocess.check_call([IPVSADM, "-Z", self.prtcmd, 
                                   self.service_addr])
            return True
        except:
            raise ValueError("could not reset counters")
    
class LVSManager():
    """class for handling LVSInstances
    """
    
    def __init__(self):
        pass
    
    def add_lvs_instance(self, service_addr, proto):
        """add new new LVS instance, will return an LVSInstance object
        
        service_addr: service_addr:port of the service to add
        proto: udp or tcp
        """
        
        validateservice_addr(service_addr)
        
        prtcmd = _prtcmd(proto)
            
        try:
            subprocess.check_call([IPVSADM, "-A", prtcmd, service_addr])
            return LVSInstance(service_addr, proto)
        except:
            raise ValueError("could not create LVS instance, "
                             "seems to already exist ")
        
    def del_lvs_instance(self, service_addr, proto):
        """deletes LVS instance
        
        service_addr: service_addr:port of the service to deleate 
        proto: udp or tcp
        """
        
        validateservice_addr(service_addr)
        
        prtcmd = _prtcmd(proto)
        
        try:
            subprocess.check_call([IPVSADM, "-D", prtcmd, service_addr])
            return True
        except:
            raise ValueError("could not delete LVS instance, already gone?")
        
    def get_lvs_instance(self, name):
        """get an LVSInstance object, for an existing Service
        
        name: is the name as returned by LVSManager.list_lvs_instances()
        """
        
        proto, service_addr = name.split('_')
        
        if proto not in PROTOS:
            raise ValueError, "Provided name looks insane, proto part is "
        "invalid: {0}".format(proto)
        
        if name in self.list_lvs_instances():
            return LVSInstance(service_addr, proto)
        else:
            raise ValueError, "{0} not found in IPVS table".format(name)
    
    def list_lvs_instances(self):
        """list all ipvs instance found in the ipvs table
        
        return a list of LVSInstance objects representing discovered LVS Services  
        """
        cmd = subprocess.Popen(["ipvsadm", "-Sn"], stdout=subprocess.PIPE)
        out, err = cmd.communicate()

        if err:
            raise ValueError("something has failed: {0}".format(err))
        
        result = []
        
        for line in out.split('\n'):
            if line.startswith("-A -t"):
                result.append(LVSInstance(line.split()[2], "tcp"))
            elif line.startswith("-A -u"):
                result.append(LVSInstance(line.split()[2], "udp"))
            else:
                continue
        return result
    
    def clear_ipvs(self):
        """clear the whole LVS table
        
        """
        try:
            subprocess.check_call([IPVSADM, "-C"])
            return True
        except:
            raise ValueError("could not clear IPVS table")
        
    def set_timeouts(self, tcp, tcpfin, udp):
        """set ipvs connection timeout values
        
        see ipvsadm manpage for details
        """
        
        tcp = str(tcp)
        tcpfin = str(tcpfin)
        udp = str(udp)
        try:
            subprocess.check_call([IPVSADM, "--set", tcp, tcpfin, udp])
            return True
        except:
            raise ValueError("could not set timeouts, "
                             "arguments seem to be invalid")
    
    def zero(self):
        """Zero the packet, byte and rate counters for all services
        """
        try:
            subprocess.check_call([IPVSADM, "-Z"])
            return True
        except:
            raise ValueError("could not reset counters")
