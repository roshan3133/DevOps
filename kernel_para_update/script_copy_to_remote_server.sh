# copy bond_mode files to remote servers.
tdate=$(date +%F)
log_file="file_copy.log"
for host in `cat iplist.txt`
do
sshpass -p redhat scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r kernel_para root@$host:/tmp/
copied=`echo $?`
if [ $copied -eq 0 ]
then
echo "$tdate -- $host files copied successfully !!!" >> $log_file
else
echo "$tdate -- $host files NOT copied" >> $log_file
fi
done
