import os.path

file_path = os.path.dirname(__file__)

fabconf = {}

# Username for connecting to EC2 instaces
fabconf['SERVER_USERNAME'] = "ubuntu"

# Full local path for .ssh
fabconf['SSH_PATH'] = "/path/to/.ssh"

# List of APT packages to install
fabconf['APT_PACKAGES'] = [
    "mysql-client", "nginx", "memcached", "git",
    "python-setuptools", "python-dev", "build-essential", "python-pip", "python-mysqldb",
    ]

# List of pypi packages to install
fabconf['PIP_PACKAGES'] = ["virtualenv", "virtualenvwrapper","supervisor"]

# Name of the private key file you use to connect to EC2 instances
fabconf['EC2_KEY_NAME'] = "key.pem"

# Don't edit. Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (fabconf['SSH_PATH'], fabconf['EC2_KEY_NAME'])

# Project name: polls
fabconf['PROJECT_NAME'] = "polls"

# Where to install apps
fabconf['APPS_DIR'] = "/home/%s/webapps" % fabconf['SERVER_USERNAME']

# Where you want your project installed: /APPS_DIR/PROJECT_NAME
fabconf['PROJECT_PATH'] = "%s/%s" % (fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

# App domains
fabconf['DOMAINS'] = "example.com www.example.com"

# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/home/%s/.virtualenvs" % fabconf['SERVER_USERNAME']

# Git username for the server
fabconf['GIT_USERNAME'] = "Server"

# Email for the server admin
fabconf['ADMIN_EMAIL'] = "webmaster@localhost"

# Name of the private key file used for github deployments
fabconf['GITHUB_DEPLOY_KEY_NAME'] = "github"

# Don't edit. Local path for deployment key you use for github
fabconf['GITHUB_DEPLOY_KEY_PATH'] = "%s/%s" % (fabconf['SSH_PATH'], fabconf['GITHUB_DEPLOY_KEY_NAME'])

# Path to the repo of the application you want to install
fabconf['GITHUB_REPO'] = "https://github.com/gcollazo/Blank-django-Project.git"

# Virtualenv activate command
fabconf['ACTIVATE'] = "source /home/%s/.virtualenvs/%s/bin/activate" % (fabconf['SERVER_USERNAME'], fabconf['PROJECT_NAME'])

# Name tag for your server instance on EC2
fabconf['INSTANCE_NAME_TAG'] = "AppServer"

# EC2 key. http://24v.co/j5ImEZ 
ec2_key = ''

# EC2 secret. http://24v.co/j5ImEZ 
ec2_secret = ''

# AMI name. http://24v.co/liLKxj 
ec2_amis = ['ami-ccf405a5']

# Name of the keypair you use in EC2. http://24v.co/ldw0HZ 
ec2_keypair = ''

# Name of the security group. http://24v.co/kl0Jyn 
ec2_secgroups = ['']

# API Name of instance type. http://24v.co/mkWvpn
ec2_instancetype = 't1.micro'