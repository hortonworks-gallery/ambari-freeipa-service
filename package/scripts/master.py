import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    import params

    cmd = 'ipa-server-install'
    cmd = cmd + ' --hostname=' + params.server_hostname
    cmd = cmd + ' --domain=' + params.server_domain
    cmd = cmd + ' --realm=' + params.server_realm
    cmd = cmd + ' --ds-password=' + params.ds_password
    cmd = cmd + ' --master-password=' + params.master_password
    cmd = cmd + ' --admin-password=' + params.admin_password
    if params.dns_setup:
        cmd = cmd + ' --setup-dns'
        cmd = cmd + ' --forwarder=' + params.dns_forwarder
    cmd = cmd + ' --unattended --debug'
    cmd = cmd + ' >> /var/log/freeipa-stdout.log'
    
    #ipa-server-install --hostname=sandbox.hortonworks.com --domain=hortonworks.com --realm=HORTONWORKS.COM --ds-password=hortonworks --master-password=hortonworks --admin-password=hortonworks --setup-dns --forwarder=8.8.8.8 --unattended
    Execute(cmd)
    
    #echo hortonworks | kinit admin
    Execute('echo ' + params.admin_password + ' | kinit admin')

  def configure(self, env):
    import params
    env.set_params(params)

  def stop(self, env):
    Execute('service ipa stop >> /var/log/freeipa-stdout.log')
      
  def start(self, env):
    import params
    Execute('service ipa start >> /var/log/freeipa-stdout.log')

  def status(self, env):
    Execute('service ipa status')


if __name__ == "__main__":
  Master().execute()
