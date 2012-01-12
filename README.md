![Fabulous Logo](http://i.imgur.com/IMyr4.png "Fabulous")
### Deploy django apps to Amazon EC2 with ONE command

First clone the project
    
    $ git clone https://github.com/gcollazo/Fabulous.git fabfile

Just change the values of __fabulous_conf.py__ and optionally __cookbook.py__:    

    $ fab ulous
    
__Make sure the cloned folder is called *fabfile*__

Fabulous will create an EC2 instance, install everything and deploy a blank django app. __All in less than 2 minutes__.

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

#### Credits
The unicorn logo is a courtesy of [Mac McRae](http://macmcrae.com/ "Mac McRae"). You can find his work at [http://macmcrae.com/](http://macmcrae.com/ "Mac McRae Illustration").

#### License
The MIT License (MIT)

Copyright (c) 2011 Giovanni Collazo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.