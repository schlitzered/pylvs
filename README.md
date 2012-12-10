pylvs
=====

Small wrapper around ipvsadm

Usage
=====

Here are some basic examples, the lib must be run with root privileges at the moment.

>>> import pylvs
>>> manager = pylvs.LVSManager()
>>> manager.list_lvs_instances()
[tcp_207.175.44.10:80, tcp_207.175.44.20:80, tcp_207.175.44.30:80, udp_207.175.44.10:80, udp_207.175.44.20:80, udp_207.175.44.30:80, tcp_[::207.175.44.10]:80, tcp_[::207.175.44.20]:80, tcp_[::207.175.44.30]:80, udp_[::207.175.44.10]:80, udp_[::207.175.44.20]:80, udp_[::207.175.44.30]:80]
>>> instance = manager.get_lvs_instance('tcp_207.175.44.10:80')
>>> instance.get_opts()
('rr', None, None)
>>> instance.list_servers()
[('192.168.10.1:81', 'masq', '1'), ('192.168.10.2:81', 'masq', '1'), ('192.168.10.3:81', 'masq', '1'), ('192.168.10.4:81', 'masq', '1'), ('192.168.10.5:81', 'masq', '1')]
instance.add_server("192.168.10.6:81", 'masq', weight = 100)
True
>>> instance.list_servers()
[('192.168.10.1:81', 'masq', '1'), ('192.168.10.2:81', 'masq', '1'), ('192.168.10.3:81', 'masq', '1'), ('192.168.10.4:81', 'masq', '1'), ('192.168.10.5:81', 'masq', '1'), ('192.168.10.6:81', 'masq', '100')]
>>> instance.edit_server("192.168.10.6:81", 'masq', weight = 10)
True
>>> instance.list_servers()
[('192.168.10.1:81', 'masq', '1'), ('192.168.10.2:81', 'masq', '1'), ('192.168.10.3:81', 'masq', '1'), ('192.168.10.4:81', 'masq', '1'), ('192.168.10.5:81', 'masq', '1'), ('192.168.10.6:81', 'masq', '10')]
>>> instance.del_server("192.168.10.6:81")
True
>>> instance.list_servers()
[('192.168.10.1:81', 'masq', '1'), ('192.168.10.2:81', 'masq', '1'), ('192.168.10.3:81', 'masq', '1'), ('192.168.10.4:81', 'masq', '1'), ('192.168.10.5:81', 'masq', '1')]

TODO
====

 - check that we have root privileges and/or can execute ipvsadm via sudo
 - extend test cases
 - add methods to get statistics from ipvsadm
