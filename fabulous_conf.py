import os.path

file_path = os.path.dirname(__file__)

fabconf = {}

# Username for connecting to EC2 instaces
fabconf['SERVER_USERNAME'] = "ubuntu"

# Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '/path/to/.ssh/key.pem'

# Project name: polls
fabconf['PROJECT_NAME'] = "polls"

# Where to install apps
fabconf['APPS_DIR'] = "/home/ubuntu/webapps"

# Where you want your project installed: /home/ubuntu/webapps/PROJECT_NAME
fabconf['PROJECT_PATH'] = "%s/%s" % (fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

# App domains
fabconf['DOMAINS'] = "example.com www.example.com"

# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/home/ubuntu/.virtualenvs"

# Git username for the server
fabconf['GIT_USERNAME'] = "Server"

# Email for the server admin
fabconf['ADMIN_EMAIL'] = "webmaster@localhost"

# Local path for deployment key you use for github
fabconf['GITHUB_DEPLOY_KEY'] = "/path/to/.ssh/github"

# Path to the repo of the application you want to install
fabconf['GITHUB_REPO'] = "https://github.com/gcollazo/Blank-django-Project.git"

# Virtualenv activate command
fabconf['ACTIVATE'] = "source /home/ubuntu/.virtualenvs/%s/bin/activate" % fabconf['PROJECT_NAME']

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