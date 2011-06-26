from fabric.api import *
from fabric.colors import red, green, yellow
from fabulous_conf import *
import boto
import time
import json


env.user = fabconf['SERVER_USERNAME']
env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']


def fab():
  """
  *** This is what you run the first time ***
  """
  print(green("Started..."))
  env.host_string = create_server()
  print(green("Waiting 30 seconds for server to boot..."))
  time.sleep(30)
  setup_servers()
  create_virtualenv()
  install_django()
  install_gunicorn()
  setup_supervisor()


def setup_servers():
  """
  Install packages for all hosts found in hosts.json
  """

  # Install packages
  print(green("Installing Packages..."))
  sudo("apt-get update -qq")
  # sudo("apt-get upgrade -qq")
  # run("echo 'mysql-server mysql-server/root_password select %s' | sudo debconf-set-selections && echo 'mysql-server mysql-server/root_password_again select %s' | sudo debconf-set-selections && sudo apt-get install -qq mysql-server" % (DB_PWD, DB_PWD))
  print(yellow("Installing mysql-client..."))
  sudo("apt-get install -qq mysql-client")
  print(yellow("Installing nginx..."))
  sudo("apt-get install -qq nginx")
  print(yellow("Installing memcached..."))
  sudo("apt-get install -qq memcached")
  print(yellow("Installing python stuff..."))
  sudo("apt-get install -qq python-setuptools python-dev build-essential python-pip")
  # sudo("apt-get install -qq python-mysqldb")
  print(yellow("Installing git..."))
  sudo("apt-get -qq install git")
  # sudo("apt-get -qq install subversion")
  print(yellow("Installing virtualenv..."))
  sudo("pip install virtualenv")
  print(yellow("Installing virtualenvwrapper..."))
  sudo("pip install virtualenvwrapper")
  print(yellow("Installing supervisor..."))
  sudo("pip install supervisor")

  # Nginx setup: serv media files and proxy all other request
  # /etc/nginx/nginx.conf
  print(yellow("Nginx setup..."))
  f = open("%s/config_files/nginx.conf" % file_path, 'r')
  config_file = f.read()
  f.close()
  run(_write_to(config_file, "~/nginx.conf"))
  sudo("mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old")
  sudo("mv ~/nginx.conf /etc/nginx/nginx.conf")
  sudo("chown root:root /etc/nginx/nginx.conf")

  # /etc/nginx/sites-enabled/default
  print(yellow("Creating app in nginx..."))
  # Load nginx-app-proxi file and insert values
  f = open("%s/config_files/nginx-app-proxy" % file_path, 'r')
  proxy_file = f.read()
  f.close()
  run(_write_to(proxy_file % fabconf, "~/%(PROJECT_NAME)s" % fabconf))
  sudo("rm -rf /etc/nginx/sites-enabled/default")
  sudo("mv ~/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s" % fabconf)
  sudo("ln -s /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s" % fabconf)
  sudo("chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s" % fabconf)

  # Restart nginx
  print(yellow("Restarting nginx..."))
  _restart_nginx()

  # Make virtualenvwrapper work
  print(yellow("Setup virtualenvwrapper..."))
  sudo("mkdir %(VIRTUALENV_DIR)s" % fabconf)
  sudo("chown -R ubuntu:ubuntu %(VIRTUALENV_DIR)s" % fabconf)
  run('echo "export WORKON_HOME=%(VIRTUALENV_DIR)s" >> ~/.profile' % fabconf)
  run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile')
  run("source ~/.profile")

  # Make a webapps alias
  print(yellow("Making 'webapps' alias for webapps folder..."))
  run("""echo "alias webapps='cd %(APPS_DIR)s'" >> ~/.profile""" % fabconf)

  # Create WebApps Folder
  print(yellow("Create webapps folder..."))
  sudo("mkdir %(APPS_DIR)s" % fabconf)
  sudo("chown -R ubuntu:ubuntu %(APPS_DIR)s" % fabconf)

  # Setup git
  print(yellow("Setup git..."))
  run("git config --global user.name %(GIT_USERNAME)s" % fabconf)
  run("git config --global user.email %(ADMIN_EMAIL)s" % fabconf)
  put(fabconf['GITHUB_DEPLOY_KEY'], "~/.ssh/%s" % fabconf['GITHUB_DEPLOY_KEY'].split('/')[-1], use_sudo=True)
  run("chmod 600 ~/.ssh/%s" % fabconf['GITHUB_DEPLOY_KEY'].split('/')[-1])
  run("""echo 'IdentityFile ~/.ssh/%s' >> ~/.ssh/config""" % fabconf['GITHUB_DEPLOY_KEY'].split('/')[-1])
  run('ssh-keyscan github.com >> ~/.ssh/known_hosts')


@hosts('')
def create_server():
  """
  Creates EC2 Instance and writes hosts.json
  """
  print(green("Creating instance..."))
  conn = boto.connect_ec2(ec2_key, ec2_secret)
  image = conn.get_all_images(ec2_amis)

  reservation = image[0].run(1, 1, ec2_keypair, ec2_secgroups,
    instance_type=ec2_instancetype)

  instance = reservation.instances[0]
  
  while instance.state == u'pending':
    print(yellow("Instance state: %s" % instance.state))
    time.sleep(10)
    instance.update()

  print(green("Instance state: %s" % instance.state))
  print(green("Public dns: %s" % instance.public_dns_name))
  
  print(green("Updating hosts.json with hostname"))
  try:
    f = open("%s/hosts.json" % file_path, "r")
    current_settings = json.loads(f.read())
    f.close()
  except IOError:
    current_settings = {"hosts":[]}
  
  f = open("%s/hosts.json" % file_path, "w")
  current_settings['hosts'].append(instance.public_dns_name)
  f.write(json.dumps(current_settings, sort_keys=True, indent=2))
  f.close()
  
  return instance.public_dns_name


def _restart_nginx():
  sudo("/etc/init.d/nginx restart")
  

def _write_to(string, path):
  return "echo '" + string + "' > " + path

  
def _append_to(string, path):
  return "echo '" + string + "' >> " + path

def create_virtualenv():
  """
  Creates a virtualenv with the PROJECT_NAME
  """
  print(yellow("Creating virtualenv..."))
  with cd(fabconf['APPS_DIR']):
    run("mkvirtualenv --no-site-packages %(PROJECT_NAME)s" % fabconf)


def install_django():
  """
  Installs django using the virtualenv named PROJECT_NAME
  """
  print(yellow("Installing django..."))
  with cd(fabconf['APPS_DIR']):
    _virtualenv_command("pip install django")
    _virtualenv_command("django-admin.py startproject %(PROJECT_NAME)s" % fabconf)


def install_gunicorn():
  """
  Installs gunicorn using the virtualenv named PROJECT_NAME
  """
  print(yellow("Installing gunicorn..."))
  with cd(fabconf['APPS_DIR']):
    _virtualenv_command("pip install gunicorn")
    print(yellow("Copying gunicorn.conf.py to project folder..."))
    put("%s/config_files/gunicorn.conf.py" % file_path, fabconf['PROJECT_PATH'], use_sudo=True)


def _virtualenv_command(command):
  with cd(fabconf['APPS_DIR']):
    sudo(fabconf['ACTIVATE'] + ' && ' + command, user=fabconf['SERVER_USERNAME'])


def setup_supervisor():
  """
  Setups supervisor using the template found in config_files/supervisord.conf
  """
  print(yellow("Seting up supervisor..."))
  sudo("echo_supervisord_conf > /etc/supervisord.conf")
  f = open("%s/config_files/supervisord.conf" % file_path, 'r')
  superv_config = f.read()
  f.close()
  sudo(_append_to(superv_config % fabconf, "/etc/supervisord.conf"))
  print(yellow("Starting supervisor..."))
  sudo("supervisord")