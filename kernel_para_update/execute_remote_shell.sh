# remote script execution remotely.
for host in `cat iplist.txt`
do
#sshpass -p redhat ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@$host "/bin/sh /tmp/kernel_para/kernel_para_update.sh"
sshpass -p redhat ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@$host /bin/sh /tmp/kernel_para/kernel_para_update.sh 
echo "Script executed !!!"
done
