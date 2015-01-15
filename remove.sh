ipa-server-install --uninstall
service ipa stop
yum remove -y "*ipa-server" bind bind-dyndb-ldap

