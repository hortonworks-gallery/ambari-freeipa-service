#!/usr/bin/env python
from resource_management import *

# server configurations
config = Script.get_config()

ds_password = config['configurations']['freeipa-config']['freeipa.server.ds.password']
admin_password = config['configurations']['freeipa-config']['freeipa.server.admin.password']
master_password = config['configurations']['freeipa-config']['freeipa.server.master.password']
server_hostname = config['configurations']['freeipa-config']['freeipa.server.hostname']
server_domain = config['configurations']['freeipa-config']['freeipa.server.domain']
server_realm = config['configurations']['freeipa-config']['freeipa.server.realm']
dns_setup = config['configurations']['freeipa-config']['freeipa.server.dns.setup']
dns_forwarder = config['configurations']['freeipa-config']['freeipa.server.dns.forwarder']


