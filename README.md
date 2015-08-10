#### An Ambari Service for FreeIPA
Ambari service for easily installing and managing FreeIPA on HDP cluster

Author: [Ali Bajwa](https://www.linkedin.com/in/aliabajwa)

##### Setup

- Download HDP 2.2 sandbox VM image (Sandbox_HDP_2.2_VMware.ova) from [Hortonworks website](http://hortonworks.com/products/hortonworks-sandbox/)
- Import Sandbox_HDP_2.2_VMware.ova into VMWare and set the VM memory size to 8GB
- Now start the VM
- After it boots up, find the IP address of the VM and add an entry into your machines hosts file e.g.
```
192.168.191.241 sandbox.hortonworks.com sandbox    
```
- Connect to the VM via SSH (password hadoop) and start Ambari server
```
ssh root@sandbox.hortonworks.com
/root/start_ambari.sh
```

- To deploy the VNC service, run below
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/hortonworks-gallery/ambari-freeipa-service.git   /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/ambari-freeipa-service   

#sandbox
sudo service ambari restart

#non sandbox
sudo service ambari-server restart
```
- Then you can click on 'Add Service' from the 'Actions' dropdown menu in the bottom left of the Ambari dashboard:

On bottom left -> Actions -> Add service -> check FreeIPA server -> Next -> Next -> Enter password -> Next -> Deploy
![Image](../master/screenshots/screenshot-vnc-config.png?raw=true)

- On successful deployment you will see the FreeIPA service as part of Ambari service and will be able to start/stop the service from here:
![Image](../master/screenshots/screenshot-vnc-stack.png?raw=true)

- When you've completed the install process, FreeIPA server will appear in Ambari 
![Image](../master/screenshots/screenshot-freeipa-stack.png?raw=true)

- You can see the parameters you configured under 'Configs' tab
![Image](../master/screenshots/screenshot-freeipa-stack-config.png?raw=true)

- One benefit to wrapping the component in Ambari service is that you can now monitor/manage this service remotely via REST API
```
export SERVICE=FreeIPAserver
export PASSWORD=admin
export AMBARI_HOST=sandbox.hortonworks.com
export CLUSTER=Sandbox

#get service status
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X GET http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#start service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#stop service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
```


- To remove the FreeIPA service: 
  - Stop the service via Ambari
  - Delete the service
  
    ```
    curl -u admin:admin -i -H 'X-Requested-By: ambari' -X DELETE http://sandbox.hortonworks.com:8080/api/v1/clusters/Sandbox/services/FreeIPAserver
    ```
  - Remove artifacts 
  
    ```
    /var/lib/ambari-server/resources/stacks/HDP/2.2/services/freeipa-stack/remove.sh
    ```

#### Import users

- As a next step, do a kinit and try importing groups/users 

```
kinit admin
#enter your admin password

ipa group-add marketing --desc marketing
ipa group-add legal --desc legal
ipa group-add hr --desc hr
ipa group-add sales --desc sales
ipa group-add finance --desc finance


#Setup LDAP users
ipa user-add  ali --first=ALI --last=BAJWA
ipa user-add  paul --first=PAUL --last=HEARMON
ipa user-add legal1 --first=legal1 --last=legal1
ipa user-add legal2 --first=legal2 --last=legal2
ipa user-add legal3 --first=legal3 --last=legal3
ipa user-add hr1 --first=hr1 --last=hr1
ipa user-add hr2 --first=hr2 --last=hr2
ipa user-add hr3 --first=hr3 --last=hr3
ipa user-add xapolicymgr --first=XAPolicy --last=Manager
ipa user-add rangeradmin --first=Ranger --last=Admin

#Add users to groups
ipa group-add-member sales --users=ali,paul
ipa group-add-member finance --users=ali,paul
ipa group-add-member legal --users=legal1,legal2,legal3
ipa group-add-member hr --users=hr1,hr2,hr3
ipa group-add-member admins --users=xapolicymgr,rangeradmin

#Set passwords for accounts: hortonworks
echo hortonworks >> tmp.txt
echo hortonworks >> tmp.txt

ipa passwd ali < tmp.txt
ipa passwd paul < tmp.txt
ipa passwd legal1 < tmp.txt
ipa passwd legal2 < tmp.txt
ipa passwd legal3 < tmp.txt
ipa passwd hr1 < tmp.txt
ipa passwd hr2 < tmp.txt
ipa passwd hr3 < tmp.txt
ipa passwd xapolicymgr < tmp.txt
ipa passwd rangeradmin < tmp.txt
rm -f tmp.txt
```


#### Browse users

- You can browse the groups/users in FreeIPA using any LDAP browser like JXplorer 
![Image](../master/screenshots/screenshot-browse-LDAP.png?raw=true)

- The FreeIPA webUI login page should come up at the below link, but for some reason logging in as admin does not seem to work (even after configuring the Firefox browser): https://sandbox.hortonworks.com/ipa/ui/
![Image](../master/screenshots/screenshot-error.png?raw=true)


