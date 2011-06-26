# Fabulous for EC2
### Deploy django apps to Amazon EC2 with ONE command

Just change the values of __fabulous_conf.py__ and run:    
    
    $ fab fab

Fabulous will create an EC2 instance, install everything and deploy your app or a blank django app. __All in less than 2 minutes__.

#### Process
* Create server on EC2
* Wait a few seconds for server to boot
* Install packages
* Create virtualenv
* Install django in virtualenv
* Install gunicorn in virtualenv
* Setup and run supervisor

#### The setup
* nginx
* gunicorn
* supervisor
* memcached
* virtualenv
* virtualenvwrapper
* git

#### Requirements
* Python 2.6.1
* Fabric 0.9.3
* Boto 2.0b4
