Provisioning a new site
=======================

# Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:
	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config 

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job 

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

/home/username
|__sites
   |__SITENAME
      |__ database
      |__ source
      |__ static
      |__ virtualenv
