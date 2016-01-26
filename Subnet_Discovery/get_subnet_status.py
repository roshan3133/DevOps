#!/usr/bin/python
#####################
#Author : Aniket Gole
#Email : roshan3133@gmail.com
#Date : 18-03-2015
#####################
#cat log |grep 'report' |awk {'print $5'} |sort | uniq
####################
import time
import MySQLdb
from contextlib import closing
import logging
from netaddr import IPNetwork
import argparse
import commands
import os
import sys
import time
import nmap
import socket

mysqlhost = ""
mysqluser = ""
mysqlpass = ""
mysqldb = ""

# Open database connection
#db = MySQLdb.connect(mysqlhost, mysqluser, mysqlpass, mysqldb)

nscan = nmap.PortScanner()
today = time.strftime("%d-%m-%Y-%H:%M")
salt_port = 4505
hyperv_port = 2179
esxi_port = 902
data = {}

def server_ping(ip):
    out = os.system("ping -c 1 %s > /dev/null" % (ip))
    if out == 0:
       return True
    else:
       return False

def socket_running(ip, port):
    result = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((ip, port))
    #result = ("sock.connect_ex(('%s', %s))" % (ip, port))
    if result == 0:
        return True
    else:
        return False

def scan_ip(ips):
    for ip in ips:
        data['ip'] = ip
        ping_out = server_ping(ip)
        if ping_out == True:
            data['live'] = "yes"
            #salt_check(ipr)
            hyperv_check = socket_running(ip, hyperv_port)
            esxi_check = socket_running(ip, esxi_port)
            if esxi_check == True:
                data['esxi'] = 'yes'
                data['status'] = 'Done'
            else:
                data['esxi'] = 'no'
            if hyperv_check == True:
                data['hyperv'] = 'yes'
                data['status'] = 'Done'
            else:
                data['hyperv'] = 'no'
            if not esxi_check == True and not hyperv_check == True:
                data['status'] = 'NotDone'
        else:
            data['live'] = 'no'
            data['esxi'] = 'no'
            data['hyperv'] = 'no'
            data['status'] = 'NotDone'
        f = open("json_db_new", "a")
        f.write(str(data) + '\n')
	print data
#with closing(db.cursor()) as cur:
#    sql_q = ('select distinct subnet from t_subnet where serverhall="%s"' % (server_hall))
#    cur.execute(sql_q)
#    subnets = cur.fetchall()
#    subnets_list = [i[0] for i in subnets]

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  #parser.add_argument("-h", "--Help", help="Script Usage: python")
  parser.add_argument("-sub", "--Subnet", nargs='*', type=str, default=None, help="Provide Subnet in sapce separeded format only if multiple.")
  parser.add_argument("-ip", "--Ipaddress", nargs='*', type=str, default=None, help="Provilde IPaddress")
  args = parser.parse_args()
  if args.Subnet:
      data['sub'] = args.Subnet[0]
      iplist = []
      for ip in IPNetwork(args.Subnet[0]):
	  ipr = str(ip)
	  iplist.append(ipr)
      scan_ip(iplist)
  elif args.Ipaddress:
     print args.Ipaddress
     #sys.exit(1)
     scan_ip(args.Ipaddress) 
  else:
    parser.print_help()
    sys.exit(1)
  f.close()
