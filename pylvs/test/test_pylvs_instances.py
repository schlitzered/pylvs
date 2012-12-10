# -*- coding: utf8 -*-
"""this Software is released under the MIT License
Copyright (c) 2012 Stephan Schultchen
"""

import pytest
import subprocess
import pylvs
import os
import inspect
        
class TestLVSInstance_tcp_207_175_44_10_Port80:
    #def __init__(self):
    #    self.instance = None
        
    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        scriptpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.check_call([scriptpath+'/ipvsadm.sh'])
        manager = pylvs.LVSManager()
        self.instance = manager.get_lvs_instance('tcp_207.175.44.10:80')

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        scriptpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.check_call([scriptpath+'/ipvsadm_cleanup.sh'])
        
    # test LVSInstance.add_server()
    # masquerading target
    # they should pass
    def test_add_server_masq(self):
        assert self.instance.add_server("192.168.10.11:81", 'masq')  == True
    
    def test_add_server_masq_weigth(self):
        assert self.instance.add_server("192.168.10.12:81", 'masq', weigth = 65535)  == True
    
    def test_add_server_masq_upper(self):
        assert self.instance.add_server("192.168.10.13:81", 'masq', upper = 10)  == True
    
    def test_add_server_masq_upper_lower(self):
        assert self.instance.add_server("192.168.10.14:81", 'masq', upper = 10, lower = 10)  == True
    
    def test_add_server_masq_weigth_upper(self):
        assert self.instance.add_server("192.168.10.15:81", 'masq', weigth = 0, upper = 10)  == True
    
    def test_add_server_masq_weigth_upper_lower(self):
        assert self.instance.add_server("192.168.10.16:81", 'masq', weigth = 10, upper = 10, lower = 10)  == True
    
    # they should fail
    def test_add_server_masq_dublicate(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.11:81', 'masq')")
    
    def test_add_server_masq_same_as_service_addr(self):
        pytest.raises(ValueError, "self.instance.add_server('207.175.44.10:81', 'masq')")
    
    def test_add_server_masq_wrong_method(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'blubber')")
    
    def test_add_server_masq_weigth_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'masq', weight = 'ui')")
    
    def test_add_server_masq_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'masq', upper = 75555)")
    
    def test_add_server_masq_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'masq', upper = 10, lower = 884642)")
    
    def test_add_server_masq_weigth_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'masq', weight = 10, upper = 'blubber')")
    
    def test_add_server_masq_weigth_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.17:81', 'masq', weight = 10, upper = 10, lower = -10)")
    
    # ipip tunnel target
    # the should pass
    def test_add_server_ipip(self):
        assert self.instance.add_server("192.168.10.21:80", 'ipip')  == True
    
    def test_add_server_ipip_weigth(self):
        assert self.instance.add_server("192.168.10.22:80", 'ipip', weigth = 65535)  == True
    
    def test_add_server_ipip_upper(self):
        assert self.instance.add_server("192.168.10.23:80", 'ipip', upper = 10)  == True
    
    def test_add_server_ipip_upper_lower(self):
        assert self.instance.add_server("192.168.10.24:80", 'ipip', upper = 10, lower = 10)  == True
    
    def test_add_server_ipip_weigth_upper(self):
        assert self.instance.add_server("192.168.10.25:80", 'ipip', weigth = 0, upper = 10)  == True
    
    def test_add_server_ipip_weigth_upper_lower(self):
        assert self.instance.add_server("192.168.10.26:80", 'ipip', weigth = 10, upper = 10, lower = 10)  == True
    
    # they should fail
    def test_add_server_ipip_dublicate(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.21:80', 'ipip')")
    
    def test_add_server_ipip_same_as_service_addr(self):
        pytest.raises(ValueError, "self.instance.add_server('207.175.44.10:80', 'ipip')")
        
    def test_add_server_ipip_wrong_method(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'blubber')")
    
    def test_add_server_ipip_wrong_port(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:81', 'ipip')")
    
    def test_add_server_ipip_weigth_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'ipip', weight = 'ui')")
    
    def test_add_server_ipip_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'ipip', upper = 75555)")
    
    def test_add_server_ipip_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'ipip', upper = 10, lower = 884642)")
    
    def test_add_server_ipip_weigth_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'ipip', weight = 10, upper = 'blubber')")
    
    def test_add_server_ipip_weigth_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.27:80', 'ipip', weight = 10, upper = 10, lower = -10)")
    
    # direct routing target
    # they should pass   
    def test_add_server_route(self):
        assert self.instance.add_server("192.168.10.31:80", 'route')  == True
    
    def test_add_server_route_weigth(self):
        assert self.instance.add_server("192.168.10.32:80", 'route', weigth = 65535)  == True
    
    def test_add_server_route_upper(self):
        assert self.instance.add_server("192.168.10.33:80", 'route', upper = 10)  == True
    
    def test_add_server_route_upper_lower(self):
        assert self.instance.add_server("192.168.10.34:80", 'route', upper = 10, lower = 10)  == True
    
    def test_add_server_route_weigth_upper(self):
        assert self.instance.add_server("192.168.10.35:80", 'route', weigth = 0, upper = 10)  == True
    
    def test_add_server_route_weigth_upper_lower(self):
        assert self.instance.add_server("192.168.10.36:80", 'route', weigth = 10, upper = 10, lower = 10)  == True
    
    # they should fail
    def test_add_server_route_dublicate(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.31:80', 'route')")
    
    def test_add_server_route_same_as_service_addr(self):
        pytest.raises(ValueError, "self.instance.add_server('207.175.44.10:80', 'route')")
        
    def test_add_server_route_wrong_method(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'blubber')")
    
    def test_add_server_route_wrong_port(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.31:81', 'route')")
    
    def test_add_server_route_weigth_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'route', weight = 'ui')")
    
    def test_add_server_route_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'route', upper = 75555)")
    
    def test_add_server_route_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'route', upper = 10, lower = 884642)")
    
    def test_add_server_route_weigth_upper_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'route', weight = 10, upper = 'blubber')")
    
    def test_add_server_route_weigth_upper_lower_out_of_range(self):
        pytest.raises(ValueError, "self.instance.add_server('192.168.10.37:80', 'route', weight = 10, upper = 10, lower = -10)")
    
    
    #test LVSInstance.edit_server()
    # masquerading target
    def test_edit_server_masq(self):
        assert self.instance.edit_server("192.168.10.16:81", 'masq')  == True
    
    def test_edit_server_masq_weigth(self):
        assert self.instance.edit_server("192.168.10.15:81", 'masq', weigth = 65535)  == True
    
    def test_edit_server_masq_upper(self):
        assert self.instance.edit_server("192.168.10.14:81", 'masq', upper = 10)  == True
    
    def test_edit_server_masq_upper_lower(self):
        assert self.instance.edit_server("192.168.10.13:81", 'masq', upper = 10, lower = 10)  == True
    
    def test_edit_server_masq_weigth_upper(self):
        assert self.instance.edit_server("192.168.10.12:81", 'masq', weigth = 0, upper = 10)  == True
    
    def test_edit_server_masq_weigth_upper_lower(self):
        assert self.instance.edit_server("192.168.10.11:81", 'masq', weigth = 10, upper = 10, lower = 10)  == True
        
    # ipip tunnel target
    def test_edit_server_ipip(self):
        assert self.instance.edit_server("192.168.10.26:80", 'ipip')  == True
    
    def test_edit_server_ipip_weigth(self):
        assert self.instance.edit_server("192.168.10.25:80", 'ipip', weigth = 65535)  == True
    
    def test_edit_server_ipip_upper(self):
        assert self.instance.edit_server("192.168.10.24:80", 'ipip', upper = 10)  == True
    
    def test_edit_server_ipip_upper_lower(self):
        assert self.instance.edit_server("192.168.10.23:80", 'ipip', upper = 10, lower = 10)  == True
    
    def test_edit_server_ipip_weigth_upper(self):
        assert self.instance.edit_server("192.168.10.22:80", 'ipip', weigth = 0, upper = 10)  == True
    
    def test_edit_server_ipip_weigth_upper_lower(self):
        assert self.instance.edit_server("192.168.10.21:80", 'ipip', weigth = 10, upper = 10, lower = 10)  == True
    
    #direct routing target
    def test_edit_server_route(self):
        assert self.instance.edit_server("192.168.10.36:80", 'route')  == True
    
    def test_edit_server_route_weigth(self):
        assert self.instance.edit_server("192.168.10.35:80", 'route', weigth = 65535)  == True
    
    def test_edit_server_route_upper(self):
        assert self.instance.edit_server("192.168.10.34:80", 'route', upper = 10)  == True
    
    def test_edit_server_route_upper_lower(self):
        assert self.instance.edit_server("192.168.10.33:80", 'route', upper = 10, lower = 10)  == True
    
    def test_edit_server_route_weigth_upper(self):
        assert self.instance.edit_server("192.168.10.32:80", 'route', weigth = 0, upper = 10)  == True
    
    def test_edit_server_route_weigth_upper_lower(self):
        assert self.instance.edit_server("192.168.10.31:80", 'route', weigth = 10, upper = 10, lower = 10)  == True
        
    #test LVSInstance.del_server (we also remove all above added servers)
    def test_del_server(self):
        targets = ["192.168.10.11:81",
                   "192.168.10.12:81",
                   "192.168.10.13:81",
                   "192.168.10.14:81",
                   "192.168.10.15:81",
                   "192.168.10.16:81",
                   "192.168.10.21:80",
                   "192.168.10.22:80",
                   "192.168.10.23:80",
                   "192.168.10.24:80",
                   "192.168.10.25:80",
                   "192.168.10.26:80",
                   "192.168.10.31:80",
                   "192.168.10.32:80",
                   "192.168.10.33:80",
                   "192.168.10.34:80",
                   "192.168.10.35:80",
                   "192.168.10.36:80"
                   ]
        for target in targets:
            assert self.instance.del_server(target)  == True
    
    # test LVSInstance.list_servers()
    def test_list_server_members(self):
        members_reference = [('192.168.10.1:81', 'masq', '1'), 
                             ('192.168.10.2:81', 'masq', '1'), 
                             ('192.168.10.3:81', 'masq', '1'), 
                             ('192.168.10.4:81', 'masq', '1'), 
                             ('192.168.10.5:81', 'masq', '1')
                            ]
        members = self.instance.list_servers()
        assert members == members_reference
    
    # test LVSInstance.set_opts() and LVSInstance.get_opts()
    def test_set_opts(self):
        SCHEDULERS = ('rr', 'wrr', 'lc', 'wlc', 'lblc', 
              'lblcr', 'dh', 'sh', 'sed', 'nq')
        for scheduler in SCHEDULERS:
            assert self.instance.set_opts(scheduler) == True
            
    def test_get_opts(self):
        assert self.instance.get_opts() == ('nq', None, None)
    
    def test_set_opts_persistence_enable(self):
        SCHEDULERS = ('rr', 'wrr', 'lc', 'wlc', 'lblc', 
              'lblcr', 'dh', 'sh', 'sed', 'nq')
        for scheduler in SCHEDULERS:
            assert self.instance.set_opts(scheduler, persistence = 120) == True
            
    def test_get_opts_persistence_enable(self):
        assert self.instance.get_opts() == ('nq', '120', None)
    
    def test_set_opts_persistence_netmask_enable(self):
        SCHEDULERS = ('rr', 'wrr', 'lc', 'wlc', 'lblc', 
              'lblcr', 'dh', 'sh', 'sed', 'nq')
        for scheduler in SCHEDULERS:
            assert self.instance.set_opts(scheduler, persistence = 120, netmask = '255.255.255.0') == True
            
    def test_get_opts_persistence_netmask_enable(self):
        assert self.instance.get_opts() == ('nq', '120', '255.255.255.0')
        
    # test LVSInstance.zero()
    def test_zero(self):
        assert self.instance.zero() == True