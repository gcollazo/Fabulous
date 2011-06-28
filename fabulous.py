from fabric.api import *
from fabric.colors import red, green, yellow
from fabulous_conf import *
import boto
import time
import json


env.user = fabconf['SERVER_USERNAME']
env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']


def ulous():
  """
  *** This is what you run the first time ***
  """
  fab()


def fab():
  """
  This does the real work for the ulous() task. Is here to provide backwards compatibility
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

  for deb in fabconf["APT_PACKAGES"]:
      print(yellow("Installing %s..." % deb))
      sudo("apt-get install -qq %s" % deb)

  for pypi in fabconf["PIP_PACKAGES"]:
      print(yellow("Installing %s..." % pypi))
      sudo("pip install %s" % pypi)

  # Nginx setup: serv media files and proxy all other request
  # /etc/nginx/nginx.conf
  print(yellow("Nginx setup..."))
  f = open("%s/config_files/nginx.conf" % file_path, 'r')
  config_file = f.read()
  f.close()
  run(_write_to(config_file, "/home/%(SERVER_USERNAME)s/nginx.conf" % fabconf))
  sudo("mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old")
  sudo("mv /home/%(SERVER_USERNAME)s/nginx.conf /etc/nginx/nginx.conf" %fabconf)
  sudo("chown root:root /etc/nginx/nginx.conf")

  # /etc/nginx/sites-enabled/default
  print(yellow("Creating app in nginx..."))
  # Load nginx-app-proxi file and insert values
  f = open("%s/config_files/nginx-app-proxy" % file_path, 'r')
  proxy_file = f.read()
  f.close()
  run(_write_to(proxy_file % fabconf, "/home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s" % fabconf))
  sudo("rm -rf /etc/nginx/sites-enabled/default")
  sudo("mv /home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s" % fabconf)
  sudo("ln -s /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s" % fabconf)
  sudo("chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s" % fabconf)

  # Restart nginx
  print(yellow("Restarting nginx..."))
  _restart_nginx()

  # Make virtualenvwrapper work
  print(yellow("Setup virtualenvwrapper..."))
  sudo("mkdir %(VIRTUALENV_DIR)s" % fabconf)
  sudo("chown -R %(SERVER_USERNAME)s: %(VIRTUALENV_DIR)s" % fabconf)
  run('echo "export WORKON_HOME=%(VIRTUALENV_DIR)s" >> /home/%(SERVER_USERNAME)s/.profile' % fabconf)
  run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/%(SERVER_USERNAME)s/.profile' % fabconf)
  run("source /home/%(SERVER_USERNAME)s/.profile" % fabconf)

  # Make a webapps alias
  print(yellow("Making 'webapps' alias for webapps folder..."))
  run("""echo "alias webapps='cd %(APPS_DIR)s'" >> /home/%(SERVER_USERNAME)s/.profile""" % fabconf)

  # Create WebApps Folder
  print(yellow("Create webapps folder..."))
  sudo("mkdir %(APPS_DIR)s" % fabconf)
  sudo("chown -R %(SERVER_USERNAME)s: %(APPS_DIR)s" % fabconf)

  # Setup git
  print(yellow("Setup git..."))
  run("git config --global user.name '%(GIT_USERNAME)s'" % fabconf)
  run("git config --global user.email '%(ADMIN_EMAIL)s'" % fabconf)
  put(fabconf['GITHUB_DEPLOY_KEY_PATH'], "/home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s" % fabconf)
  run("chmod 600 /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s" % fabconf)
  run("""echo 'IdentityFile /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s' >> /home/%(SERVER_USERNAME)s/.ssh/config""" % fabconf)
  run('ssh-keyscan github.com >> /home/%(SERVER_USERNAME)s/.ssh/known_hosts' % fabconf)


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
  conn.create_tags([instance.id], {"Name":fabconf['INSTANCE_NAME_TAG']})
  
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
    put("%s/config_files/gunicorn.conf.py" % file_path, fabconf['PROJECT_PATH'])


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