#!/usr/bin/python
#===========================
#Author : - Aniket Gole
#===========================
from flask import Flask, render_template
import pwd
import commands
import crypt
app = Flask(__name__)

@app.route("/user_operation", methods=["POST", "GET"])
def user_operation():
    if request.method == 'GET':
      return render_template('index.html')
    if request.method == 'POST':
      username = request.form.get("uname")
      password = request.form.get("passwd")
      shell = request.form.get("shell")
      home = request.form.get("home")
      sudo = request.form.get("access")
      action = request.form.get("ops")
      print username, password, shell, home, sudo, action 
      ck_usr = check_user(username)
      if action == 'Create' and ck_usr == False:
        print action
        cr_user = create_user(username,password,shell,home,sudo)
        print cr_user
        if cr_user == True:
 	  return render_template('index.html', info=("User %s Created Successfully !!! You can create/delete/modify more users if you wish." % (username)))
        else:
          return render_template('index.html', info=("User %s Not created becasue %s" % (username, cr_user))) 
      elif action == 'Create' and ck_usr == True:
	return render_template('index.html', info=("User %s already exist" % (username)))
      elif action == 'Delete' and ck_usr == True:
        print "Deleting user"
        del_usr = delete_user(username)
        if del_usr == True:
  	  return render_template('index.html', info=("User %s Deleted successfully !!!" % (username)))
        else:
  	  return render_template('index.html', info=("User %s Not deleted, Please try again." % (username)))
      elif action == 'Modify' and ck_usr == True:
        print "Modifying user."
        modf_usr = modify_user(username) 
      else:
        "Action not selected."
def check_user(user):
  print ("Checking %s user exist or not." % (user))
  try:
    pwd.getpwnam(user)
    return True
  except KeyError:
    return False
def delete_user(user):
  print ("%s user deletion." % (user))
  cmd = ("userdel -r %s" % (user))
  reply = commands.getstatusoutput(cmd)
  print reply
  if reply[0] == 0:
    return True
def modify_user(user):
  print ("% user modification." % (user))
def create_user(user, passwd, shell, home, sudo):
  encPass = crypt.crypt(passwd,"122")   
  #return  os.system("useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ name+"\" " + username)
  print ("%s User Creation." % (user))
  #try:
  cmd = ("useradd -p %s -s %s -d %s%s -m %s" % (encPass,shell,home,user,user))
  reply = commands.getstatusoutput(cmd)
  print reply
  if reply[0] == 0:
    if sudo == 'yes':
      commands.getstatusoutput("usermod -a -G sudo "+user)
    return True
  else:
    return reply[1]
  #except:
    #return False
    
#===============Main method==================================
# Main
if __name__ == '__main__':
    #app.run(host='127.0.0.1', debug=True)
    app.run(host='192.168.1.108', debug=True)
