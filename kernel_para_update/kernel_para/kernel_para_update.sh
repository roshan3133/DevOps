# Kernel parameter Update
# Author: Aniket Gole
# Email: roshan3133@gmail.com
# Date : 28/05/2015
# This script will update kernel para as follows:
# If parameter exist the it replaced with required value.
# If parameter not exist it will add parameter with value at the end of the line.
#####################

shell=`which sh`
new_file="/tmp/sysctl.conf.new"
orig_file="/tmp/sysctl.conf.orig"
k_para_file="/tmp/kernel_para/kernel_para.txt"
log_file="/tmp/kernel_para.log"
rc_file="/tmp/kernel_para/rc.txt"
limits_file="/tmp/kernel_para/limits.txt"
cmd="/tmp/kernel_para/command"
tdate=$(date +%F)

exit 0
#echo $tdate
touch $log_file
echo "========Sysctl.conf file going to updating=============" >> $log_file
cp -ap /etc/sysctl.conf $new_file
cp -ap /etc/sysctl.conf $orig_file
#for para in `k_para.txt | awk {'print $1'}`
#for para in `cat k_para.txt`
#sed -i 's/net.ipv4.conf.all.log_martians.*/net.ipv4.conf.all.log_martians = 22/' /tmp/sysctl.conf
cat $k_para_file | while read LINE ; do
  p_name=`echo $LINE | awk {'print $1'}`
  #echo "para with value $LINE"
  #echo "para $p_name"
  echo "$tdate Updating paramter $p_name" >> $log_file
  p_exist=`cat $new_file | grep -v '#' | grep $p_name`
  #p_grep=`cat /tmp/sysctl.conf | grep -v '#' | grep 'net.ipv4.conf.all.log_martians'` 
  p_exist=`echo $?`
  #echo $p_exist
  #echo $p_grep
  if [ $p_exist -eq 1 ]
  then
    echo $LINE >> $new_file
    echo "Appending paramter $LINE" >> $log_file
  else 
    #echo "0" 
    sed -i 's/$p_name.*/$LINE/' $new_file
    echo "Changing paramter value $LINE" >> $log_file
  fi
done
# Uncomment below two line if you really want to update /tmp/sysctl.conf.new into /etc/sysctl.conf
cp -ap $new_file /etc/sysctl.conf
sysctl -p
echo "========Sysctl.conf file updated=============" >> $log_file
############################ End of sysctl ########################################################
if [ -s "$limits_file" ]
then
  cat $limits_file >> /etc/security/limits.conf
  echo "/etc/limits.conf file updated." >> $log_file
else
  echo "$limits_file file empty so /etc/limits.conf file not updated." >> $log_file
fi
########################
if [ -s "$cmd" ]
then 
   $shell $cmd
   echo "Commands executed." >> $log_file
else
   echo "$cmd file empty so command does not execute." >> $log_file
fi
########################
if [ -s "$rc_file" ]
then
  cat $rc_file >> /etc/rc.local
  echo "$rc_file Updated in /etc/rc.local" >> $log_file
else
  echo "$rc_file empty so no update" >> $log_file
fi
#####################

