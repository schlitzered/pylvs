# -*- coding: utf8 -*-
"""this Software is released under the MIT License
Copyright (c) 2012 Stephan Schultchen
"""

import pytest
import subprocess
import pylvs
import os
import inspect
        
class Test_LVSManager:
    
    def _initlvs(self):
        scriptpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.check_call([scriptpath+'/ipvsadm.sh'])

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        pass

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        scriptpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.check_call([scriptpath+'/ipvsadm_cleanup.sh'])

    # validate LVSManager.add_lvs_instance
    def test_add_lvs_instance(self):
        options = (("192.168.10.10:80", "tcp"), 
                   ("192.168.10.10:80", "udp"),
                   ("[::192.168.10.10]:80", "tcp"),
                   ("[::192.168.10.10]:80", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            assert manager.add_lvs_instance(service_addr, proto) == proto+"_"+service_addr

    def test_add_lvs_instance_duplicate(self):
        options = (("207.175.44.10:80", "tcp"), 
                   ("207.175.44.10:80", "udp"),
                   ("[::207.175.44.10]:80", "tcp"),
                   ("[::207.175.44.10]:80", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.add_lvs_instance(service_addr, proto)")
    
    def test_add_lvs_instance_invalid_ip(self):
        options = (("207.175.666.10:80", "tcp"), 
                   ("207.175.44.666:80", "udp"),
                   ("[::207.175.666.10]:80", "tcp"),
                   ("[::207.175.666.10]:80", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.add_lvs_instance(service_addr, proto)")
        
    def test_add_lvs_instance_invalid_port(self):
        options = (("192.168.10.10:-80", "tcp"), 
                   ("192.168.10.10:75684", "udp"),
                   ("[::192.168.10.10]:1.65", "tcp"),
                   ("[::192.168.10.10]:-1.65", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.add_lvs_instance(service_addr, proto)")
    
    def test_add_lvs_instance_invalid_proto(self):
        options = (("192.168.10.10:80", "fwmark"), 
                   ("192.168.10.10:80", "fwmark"),
                   ("[::192.168.10.10]:80", "fwmark"),
                   ("[::192.168.10.10]:80", "fwmark"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.add_lvs_instance(service_addr, proto)")
    
    # validate LVSManager.del_lvs_instance
    def test_del_lvs_instance(self):
        options = (("207.175.44.10:80", "tcp"), 
                   ("207.175.44.10:80", "udp"),
                   ("[::207.175.44.10]:80", "tcp"),
                   ("[::207.175.44.10]:80", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            assert manager.del_lvs_instance(service_addr, proto) == True
        
    def test_del_lvs_instance_non_existent(self):
        options = (("207.175.44.11:80", "tcp"), 
                   ("207.175.44.10:81", "udp"),
                   ("[::207.175.44.11]:80", "tcp"),
                   ("[::207.175.44.10]:81", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.del_lvs_instance(service_addr, proto)")
        
    def test_del_lvs_instance_invalid_ip(self):
        options = (("192.168.666.10:80", "tcp"), 
                   ("192.168.10.666:80", "udp"),
                   ("[::207.175.666.11]:80", "tcp"),
                   ("[::207.175.44.666]:80", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.del_lvs_instance(service_addr, proto)")
        
    def test_del_lvs_instance_invalid_port(self):
        options = (("207.175.44.10:-80", "tcp"), 
                   ("207.175.44.10:75896", "udp"),
                   ("[::207.175.44.10]:1.65", "tcp"),
                   ("[::207.175.44.10]:.1.65", "udp"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.del_lvs_instance(service_addr, proto)")
    
    def test_del_lvs_instance_invalid_proto(self):
        options = (("207.175.44.10:80", "fwmark"), 
                   ("207.175.44.10:80", "fwmark"),
                   ("[::207.175.44.10]:80", "fwmark"),
                   ("[::207.175.44.10]:80", "fwmark"),
                   )
        for i in options:
            service_addr, proto = i
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.del_lvs_instance(service_addr, proto)")
    
    def test_get_lvs_instance(self):
        options = ("tcp_207.175.44.10:80", 
                   "udp_207.175.44.10:80",
                   "tcp_[::207.175.44.10]:80",
                   "udp_[::207.175.44.10]:80",
                   )
        for name in options:
            self._initlvs()
            manager = pylvs.LVSManager()
            assert manager.get_lvs_instance(name) == name
    
    def test_get_lvs_instance_invalid(self):
        options = ("tcp_207.175.44.11:80", 
                   "udp_207.175.44.10:81",
                   "tcp_[::207.175.44.11]:80",
                   "udp_[::207.175.44.10]:81",
                   )
        for name in options:
            self._initlvs()
            manager = pylvs.LVSManager()
            pytest.raises(ValueError, "manager.get_lvs_instance(name)")
    
    def test_list_lvs_instances_count(self):
        self._initlvs()
        manager = pylvs.LVSManager()
        assert len(manager.list_lvs_instances()) == 12
        
    def test_list_lvs_instances_members(self):
        self._initlvs()
        manager = pylvs.LVSManager()
        instances_a = ["tcp_207.175.44.10:80", 
                     "tcp_207.175.44.20:80", 
                     "tcp_207.175.44.30:80", 
                     "udp_207.175.44.10:80", 
                     "udp_207.175.44.20:80", 
                     "udp_207.175.44.30:80", 
                     "tcp_[::207.175.44.10]:80", 
                     "tcp_[::207.175.44.20]:80", 
                     "tcp_[::207.175.44.30]:80", 
                     "udp_[::207.175.44.10]:80", 
                     "udp_[::207.175.44.20]:80", 
                     "udp_[::207.175.44.30]:80"]
        instances_b = manager.list_lvs_instances()
        
        for i in instances_a:
            assert i in instances_b
    
    def test_clear_ipvs(self):
        self._initlvs()
        manager = pylvs.LVSManager()
        assert manager.clear_ipvs() == True
    
    def test_set_timeouts(self):
        self._initlvs()
        manager = pylvs.LVSManager()
        assert manager.set_timeouts(10, 10, 10) == True
        
    def test_zero(self):
        self._initlvs()
        manager = pylvs.LVSManager()
        assert manager.zero() == True