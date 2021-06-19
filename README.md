# CyberSmarties Registration Module

Registration page for CyberSmarties India

![CyberSmarties Logo](static/registration/images/logo2.png)

------



# Deploying Django with Apache and mod_wsgi on Ubuntu



## Basics Walkthrough.

### What’s the Django Framework?

**Django** is a powerful Python web framework that helps us to develop web applications very easily. It is used to combine HTML/CSS, JavaScript files for front-end, and python for the back-end. Django includes a simplified development server for testing our application on the local machine, but for slightly production-related work we need a more secure and powerful server.

### What is Web Server Gateway Interface?

Web Server Gateway Interface (WSGI)is just an ***interface*** specification with which, the ***server and application communicate.***
A WSGI server (meaning WSGI compliant) only ***receives the request from the client, passes it to the application and then sends the response*** returned by the application to the client. It is only used for Python Programming Language.

An HTTP web server’s primary task is to receive a request, and serve HTTP files in response. [**Apache**](https://httpd.apache.org/) is an example of an HTTP web server.
The caveat here is that that Apache at its core, is designed to serve only HTTP requests. This is where different modules for Apache comes in. These modules help Apache perform various functions.

A module called [**mod-wsgi**](https://modwsgi.readthedocs.io/) will be used to help **Apache communicate with WSGI interface** in our Django application.



## Prerequisites

- You should have a fresh latest Ubuntu server instance with a non-root user with `sudo` privileges configured and running.
- SSH connection to your server.
- Security Group configured to allow all access to port 22(SSH), 80(HTTP), 443(HTTPS) and 8000(testing Django development server)



## Install Packages from the Ubuntu Repositories

To begin the process, we’ll download and install all of the items we need from the Ubuntu repositories. This will include the Apache web server, the `mod_wsgi` module used to interface with our Django app, and `pip`, the Python package manager that can be used to download our Python-related tools.

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
```

The First command is to update the **apt package manager** in Ubuntu. The second command is used to install apache2, pip3, and `mod-wsgi`(module used in Apache, for running Django server).

**Note:** here `sudo` is used to provide root access whenever necessary.



## Configure a Python Virtual Environment on Ubuntu

### Install virtualenv and Create a Virtual Environment

Now that we have the component from the ubuntu machine, we can start working on our Django project. The first step is to create a Python virtual environment so that our Django project will be separated from the system tools and other python projects we may be working on. Install the `virtualenv` package using the following command.

```shell
sudo pip3 install virtualenv
```

With `virtualenv `installed, we can start forming our project. Create a directory where we wish to keep our project and move into that directory.

```shell
mkdir django
cd django
```

Here we will set up our virtual environment and also clone our Django application repository from GitHub.

Now, within the directory, create a Python virtual environment by typing:

```shell
virtualenv mydjangoenv
```

This will create a directory call `mydjangoenv` within our Django directory.

Before we will install our project’s Python requirements, we need to activate the virtual environment.

We can do this by typing:

```shell
source /home/ubuntu/django/mydjangoenv/bin/activate
```

Our prompt should change to indicate that we are now operating within a Python virtual environment. It will look something like this: `(mydjangoenv) user@host:~/django$.`

### Clone Django Project from GitHub and Install Requirements

Now clone the GitHub repository where our Django application located.

```shell
git clone "https://github.com/ryanmauriya/registration.git"
```

**In this article, the repository name is taken as** `registration`**.** This will create a directory call `registration` within our Django directory.

Now we are ready to install necessary requirements, run the following command:

```shell
pip install -r registration/requirements.txt
```

*The most important dependency is Django which can be installed or updated by running following command. Don't run this if you don't want to update Django*  

```shell
$ pip install django
```



## Running the Django development server.

### Adjust the Project Settings

We have to edit the `settings.py` file of the Django project.

```shell
sudo nano registration/CySm/settings.py
```

I like `nano` text editor more than `vim` because its easier 😊.  Add the below line to `settings.py` if it does not exist.

```python
STATIC_ROOT = os.path.join(BASE_DIR, “static”)
```

This line specifies the directory where all the static files of the application are located.

Also, we have to add instance’s DNS name/IP to “Allowed Hosts” in `settings.py`.

```python
ALLOWED_HOSTS = [‘EC2_DNS_NAME/IP’, 'sub.domain-name.com']
```

Press `Ctrl+O` and `Enter` to write changes and `Ctrl+X` to exit `nano`.

### Complete Initial Project Setup

Now, we can migrate the initial database schema to our SQLite database using the management script:

```bash
cd registration/
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

Create an administrative user for the project by typing:

```bash
python manage.py createsuperuser
```

You will have to select a username, provide an email address, and choose and confirm a password.

We can collect all of the static content into the directory location we configured by typing:

```bash
python manage.py collectstatic
```

 You will have to confirm the operation. The static files will be placed in a directory called `static` within your project directory.

### Run Development Server

Finally, you can test your project by starting up the Django development server with this command:

```bash
python manage.py runserver 0.0.0.0:8000
```

In the browser, visit IP of the instance, make sure to append post “8000” at the end of the URL, and if everything goes fine we will see our Django application running in the browser 👍.

```http
http://server_domain_or_IP:8000/
```

This might work for some time now, but as soon as the SSH connection is broken/closed, or the instance is rebooted, the server will stop and thus will not respond to requests.

**To resolve this issue, we use the Apache server. It means that the Apache server always keeps running in the background, and keeps on responding to users requesting for data and files. This is where the robustness of the Apache server outshines the development server of Django.**

When you are finished exploring, hit `CTRL+C` in the terminal window to shut down the development server.

We’re now done with Django for the time being, so we can back out of our virtual environment by typing:

```bash
deactivate
```

***We can now remove the security group entry for port 8000. Recommended for security reasons.***



## Configure Apache Server

Virtual host files are the files that specify the actual configuration of our virtual hosts and dictate how the Apache web server will respond to various domain requests.

Apache comes with a default virtual host file called `000-default.conf` that we can use as a jumping off point. We are going to copy it over to create a virtual host file for each of our domains.

### Create New Virtual Host File

Start by copying the default virtual host file.

```bash
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/registration.cybersmarties.in.conf
```

To configure WSGI pass we’ll need to edit `registration.cybersmarties.in.conf` file:

```bash
sudo nano /etc/apache2/sites-available/registration.cybersmarties.in.conf
```

Replace the file with the following configuration:

```
<VirtualHost *:80>
ServerName registration.cybersmarties.in
#ServerAlias www.example.com
ServerAdmin webmaster@example.com
DocumentRoot /home/ubuntu/django/registration
ErrorLog ${APACHE_LOG_DIR}/django_error.log
CustomLog ${APACHE_LOG_DIR}/django_access.log combined
Alias /static /home/ubuntu/django/registration/static
<Directory /home/ubuntu/django/registration/static>
Require all granted
</Directory>
<Directory /home/ubuntu/django/registration/CySm>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
WSGIDaemonProcess djangoproj python-path=/home/ubuntu/django/registration python-home=/home/ubuntu/django/mydjangoenv
WSGIProcessGroup djangoproj
WSGIScriptAlias / /home/ubuntu/django/registration/CySm/wsgi.py
</VirtualHost>
```

- The first line specifies that* **Apache will listen to port 80** (default HTTP), and serve the files specified.

- change the `ServerAdmin` directive to an email that the site administrator can receive emails through

- `ServerName`, establishes the base domain that should match for this virtual host definition. This will most likely be your domain. `ServerAlias`, defines further names that should match as if they were the base name. This is useful for matching hosts you defined, like `www`:

  ```
  ServerName example.com
  ServerAlias www.example.com
  ```

  *We don't need these two for now. But will be used for enabling custom domain and https on apache.*

- Document root specifies the location of the application files.

- The directory tags are used to give Apache server the permission to access the respective directory and its files.

- The WSGI settings are required for the Django server to work. `python-home` is set to path of virtual environment.

- Please make sure the paths are correct and according to naming of directories and files in the Django project.

### Enable the New Virtual Host File

Now that we have created our virtual host files, we must enable them. Apache includes some tools that allow us to do this.

We’ll be using the `a2ensite` tool to enable each of our sites. If you would like to read more about this script, you can refer to the [a2ensite documentation](https://manpages.debian.org/jessie/apache2/a2ensite.8.en.html).

```bash
sudo a2ensite registration.cybersmarties.in.conf
```

 Next, disable the default site defined in `000-default.conf`:

```bash
sudo a2dissite 000-default.conf
```

Check your Apache files to make sure you did not make any syntax errors:

```bash
sudo apache2ctl configtest
```

As long as the last line of output looks like this, your files are in good shape:

```bash
Syntax OK
```

 When you are finished, you need to restart Apache to make these changes take effect and use `systemctl status` to verify the success of the restart.

```bash
sudo systemctl restart apache2
sudo systemctl status apache2
```

 You should now be able to access your Django site by going to your server’s domain name or IP address without specifying a port like this `http://server_domain_or_IP/`. The regular site and the admin interface should function as expected.

### Wrapping Up Some Permissions Issues

If you are using the **SQLite database**, which is the default used in this article, **you need to allow the Apache process access to this file**.

To do so, the first step is to change the permissions so that the group owner of the database can read and write. The database file is called `db.sqlite3` by default and it should be located in your base project directory `/django/registration` :

```bash
chmod 664 db.sqlite3
```

Afterwards, we need to give the group Apache runs under, the `www-data` group, group ownership of the file:

```bash
sudo chown :www-data db.sqlite3
```

***Note:*** *Run the above two commands to reapply the permissions if `db.sqlite3` is deleted in anyway.*

In order to write to the file, we also need to give the Apache group ownership over the database’s parent directory:

```bash
sudo chown :www-data /home/ubuntu/django/registration
```

Now we need to **give permission to the `registration/media/` folder**. In order for my app to be able upload media files, we needed to change the permissions and owner settings. This sounded scary at first, but doesn’t have to be. [This Stack Overflow answer](https://stackoverflow.com/questions/21797372/django-errno-13-permission-denied-var-www-media-animals-user-uploads?answertab=votes#answer-21797786) and [File Permissions for Django Media Uploads](https://www.adamerispaha.com/2016/12/14/file-permissions-for-django-media-uploads/) was extremely helpful.

```bash
sudo groupadd registrationmedia
sudo adduser www-data registrationmedia
sudo chgrp -R registrationmedia /home/ubuntu/django/registration/media
sudo chmod -R 760 /home/ubuntu/django/registration/media
```

### Set Up a Basic Firewall 🔥

Ubuntu servers can use the UFW firewall to make sure only connections to certain services are allowed. We can set up a basic firewall very easily using this application.

Different applications can register their profiles with UFW upon installation. These profiles allow UFW to manage these applications by name. OpenSSH, the service allowing us to connect to our server now, has a profile registered with UFW.

You can see this by typing:

```bash
sudo ufw app list
```

```bash
Available applications:
  Apache
  Apache Full
  Apache Secure
  OpenSSH
```

We need to make sure that the firewall allows SSH connections so that we can log back in next time. We can allow these connections by typing:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Apache Full'
```

Afterwards, we can enable the firewall by typing:

```bash
sudo ufw enable
```

Type “y” and press ENTER to proceed. You can see that SSH connections are still allowed by typing:

```bash
sudo ufw status
```

```bash
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Apache Full                ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
Apache Full (v6)           ALLOW       Anywhere (v6)
```

If you install and configure additional services, you will need to adjust the firewall settings to allow acceptable traffic in. You can learn some common UFW operations in [this guide](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands).

### It works 😀

Now ***navigate to public DNS/IP of the instance in the browser*** and one shall see the Django application running if everything was set up correctly, the page of victory. 👍

This was just an example of how to setup **Django with Apache** on cloud service.
There are a lot of other factors that come into play when deploying a production server.
One of the most important areas of attention is **Security.**

To make the server more secure, one can limit it’s access to a few IP addresses which should be ideal for development and testing.

For all of these purposes, AWS tools like [Security Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html) and [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) users can come handy.

One can also use [AWS beanstalk](https://aws.amazon.com/elasticbeanstalk/) service to deploy Django apps in an easier way.

Reference: [Django documentation](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/)



## Coming Up

After verifying that your application is accessible, it is important to secure traffic to your application.

If you have a domain name for your application, the easiest way to secure your application is with a free SSL certificate from Let’s Encrypt. Follow [How To Secure Apache with Let's Encrypt on Ubuntu](#Enable HTTPS with Let's Encrypt SSL on Ubuntu) to learn how to set this up.

If you **do not** have a domain name for your application and are using this for your own purposes or for testing, you can always create a self-signed certificate. You can learn how to set this up with [How To Create a Self-Signed SSL Certificate for Apache in Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-18-04).

------



# Enable HTTPS with Let's Encrypt SSL on Ubuntu



## What is Let's Encrypt

<p align="center"><img src="https://letsencrypt.org/images/le-logo-twitter-noalpha.png" alt="Let's Encrypt" width="400" /></p>

Let’s Encrypt is a Certificate Authority (CA) that facilitates obtaining and installing free [TLS/SSL certificates](https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs), thereby enabling encrypted HTTPS on web servers. It simplifies the process by providing a software client, Certbot, that attempts to automate most (if not all) of the required steps. Currently, the entire process of obtaining and installing a certificate is fully automated on both Apache and Nginx.

In this guide, we’ll use [Certbot](https://certbot.eff.org/) to obtain a free SSL certificate for Apache on Ubuntu 20.04, and make sure this certificate is set up to renew automatically.



## Prerequisites

To follow this tutorial, you will need:

- Django deployed with Apache on Ubuntu server instance set up by following this [Deploying Django with Apache and mod_wsgi on Ubuntu](#deploying-django-with-apache-and-mod_wsgi-on-ubuntu) tutorial, including a sudo non-root user and a firewall.
- A fully registered domain name. This tutorial will use **your_domain **(eg. cybersmarties.com) as an example throughout.
- Allow all access to HTTPS port 443 in server settings.
- Static IPv4 address for the server instance. In AWS this is called [Elastic IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)
- Basic nano(command line text editor) usage since there will be some editing 😒.



## Using Custom Domain Name for Our Application

We deployed our site in a Linux server but we are still accessing the site using our IP address. Now we will see how to setup a domain name so that when we navigate to our domain, its takes us to the Django application.

Now we need both of the following DNS records set up for your server. You can follow [point domain name to an IP address](https://www.123-reg.co.uk/support/domains/how-do-i-point-my-domain-name-to-an-ip-address/) for details on how to add them.

- An A record with `your_domain` pointing to your server’s public IP address.
- An A record with `www.your_domain` pointing to your server’s public IP address.

This will vary based on your *domain registrar* and *server hosting*. **I recommend searching for tutorials from your domain registrar.**

If you have **AWS** hosting follow this [How to Link Your Domain Name With AWS EC2](https://youtu.be/qor31Egu0Rg) tutorial.

If you have **DigitalOcean** follow [this introduction to DigitalOcean DNS](https://www.digitalocean.com/community/tutorials/an-introduction-to-digitalocean-dns) for details.

We recommend creating new Apache virtual host files for each domain hosted in a server, because it helps to avoid common mistakes and maintains the default configuration files as a fallback setup.

So we will change the name of the virtual host file we previously created `/etc/apache2/sites-available/registration.cybersmarties.in.conf` to `/etc/apache2/sites-available/your_domain.conf`. Run the following commands to do this:

```bash
sudo a2dissite registration.cybersmarties.in.conf
sudo mv /etc/apache2/sites-available/registration.cybersmarties.in.conf /etc/apache2/sites-available/your_domain.conf
sudo a2ensite your_domain.conf
```

Now if you should have a virtual host block set up for your domain at `/etc/apache2/sites-available/your_domain.conf` with the `ServerName` and also the `ServerAlias` directives.

open the virtual host file for your domain using `nano` or your preferred text editor:

```bash
sudo nano /etc/apache2/sites-available/your_domain.conf
```

Find the existing `ServerName` and `ServerAlias` lines and uncomment `ServerAlias`. They should look like this:

```bash
...
ServerName your_domain
ServerAlias www.your_domain
...
```

If you already have your `ServerName` and `ServerAlias` set up like this, you can exit your text editor and move on to the next step. If you’re using `nano`, you can exit by typing `CTRL+X`, then `Y` and `ENTER` to confirm.

Then, run the following command to validate your changes:

```bash
sudo apache2ctl configtest
```

You should get a `Syntax OK` as a response. Restart Apache so that the changes take effect:

```bash
sudo systemctl restart apache2
```

Make sure you **add your_domain and www.your_domain to ALLOWED_HOSTS** in `settings.py` file. Read this [section](#adjust-the-project-settings) for instruction.

With these changes, you should now be able to access your Django site by going to your server’s domain name like this `http://your_domain/` or `http://www.your_domain/` .

***Note*** *that it is still HTTP and not HTTPS so we are not done yet. You can see that the site says its not secure (no 🔒) in the URL bar. For HTTPS to work we need to get an SSL Certificate. We will see that in the next section.*



## Installing Certbot

### Install snapd

Ubuntu 16 and above comes preinstalled with snap. Follow these instructions on [snapcraft's site to install snapd](https://snapcraft.io/docs/installing-snapd/).

Ensure that your version of snapd is up to date. Execute the following instructions on the command line on the machine to ensure that you have the latest version of `snapd`.

```
sudo snap install core; sudo snap refresh core
```

### Remove certbot-auto and any Certbot OS packages

If you have any Certbot packages installed using an OS package manager like `apt`, `dnf`, or `yum`, you should remove them before installing the Certbot snap to ensure that when you run the command `certbot` the snap is used rather than the installation from your OS package manager. The exact command to do this depends on your OS, but common examples are `sudo apt-get remove certbot`, `sudo dnf remove certbot`, or `sudo yum remove certbot`.

If you previously used Certbot through the certbot-auto script, you should also remove its installation by following the instructions [here](https://certbot.eff.org/docs/uninstall.html).

### Install Certbot

Run this command on the command line on the machine to install Certbot.

```
sudo snap install --classic certbot
```

### Prepare the Certbot command

Execute the following instruction on the command line on the machine to ensure that the `certbot` command can be run.

```
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```



## Obtaining an SSL Certificate

We are now ready to run the certbot command. But first we actually need to make a change to one of our config file at this point because we will run into problem if we don't make a couple of changes.

We need to comment some of the lines in `/etc/apache2/sites-available/your_domain.conf` so we open it up using nano.

```bash
sudo nano /etc/apache2/sites-available/your_domain.conf
```

Comment the following lines so that it looks some thing like this:

```bash
...
#WSGIDaemonProcess djangoproj python-path=/home/ubuntu/django/registration python-home=/home/ubuntu/django/mydjangoenv
#WSGIProcessGroup djangoproj
#WSGIScriptAlias / /home/ubuntu/django/registration/CySm/wsgi.py
...

```

Hit `Ctrl+X` and `Enter` to save the changes. Now we can run certbot command.

Certbot provides a variety of ways to obtain SSL certificates through plugins. The Apache plugin will take care of reconfiguring Apache and reloading the configuration whenever necessary. To use this plugin, type the following:

```bash
sudo certbot --apache
```

This script will prompt you to answer a series of questions in order to configure your SSL certificate. First, it will ask you for a valid e-mail address. This email will be used for renewal notifications and security notices:

After providing a valid e-mail address, hit `ENTER` to proceed to the next step. You will then be prompted to confirm if you agree to Let’s Encrypt terms of service. You can confirm by pressing `A` and then `ENTER`:

Next, you’ll be asked if you would like to share your email with the Electronic Frontier Foundation to receive news and other information. If you do not want to subscribe to their content, type `N`. Otherwise, type `Y`. Then, hit `ENTER` to proceed to the next step.

The next step will prompt you to inform Certbot of which domains you’d like to activate HTTPS for. The listed domain names are automatically obtained from your Apache virtual host configuration, that’s why it’s important to make sure you have the correct `ServerName` and `ServerAlias` settings configured in your virtual host. If you’d like to enable HTTPS for all listed domain names (recommended), you can leave the prompt blank and hit `ENTER` to proceed. Otherwise, select the domains you want to enable HTTPS for by listing each appropriate number, separated by commas and/ or spaces, then hit `ENTER`.

```
Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: your_domain
2: www.your_domain
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel):
```

You’ll see output like this:

```
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for your_domain
http-01 challenge for www.your_domain
Enabled Apache rewrite module
Waiting for verification...
Cleaning up challenges
Created an SSL vhost at /etc/apache2/sites-available/your_domain-le-ssl.conf
Enabled Apache socache_shmcb module
Enabled Apache ssl module
Deploying Certificate to VirtualHost /etc/apache2/sites-available/your_domain-le-ssl.conf
Enabling available site: /etc/apache2/sites-available/your_domain-le-ssl.conf
Deploying Certificate to VirtualHost /etc/apache2/sites-available/your_domain-le-ssl.conf
```

After this step, Certbot’s configuration is finished, and you will be presented with the final remarks about your new certificate, where to locate the generated files, and how to test your configuration using an external tool that analyzes your certificate’s authenticity:

```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations! You have successfully enabled https://your_domain and
https://www.your_domain

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=your_domain
https://www.ssllabs.com/ssltest/analyze.html?d=www.your_domain
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/your_domain/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/your_domain/privkey.pem
   Your cert will expire on 2020-07-27. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

Your certificate is now installed and loaded into Apache’s configuration. Certbot has created a file with the name `your_domain-le-ssl.conf ` (which is basically a copy of `your_domain.conf` with some extra lines) in `/etc/apache2/sites-available` directory. It also appended `RewriteEngine on` to `your_domain.conf` so that the HTTP link is redirected to the secure HTTPS link.

Now before we can access the application on our browser, we need to edit some config files. We can comment off all the lines in `your_domain.conf` except the RewriteEngine since we will no longer be using the HTTP site and we will be using the HTTPS. RewriteEngine should NOT be commented because it redirects the site from HTTP to HTTPS. So edit this file so that the output looks like this:

```bash
sudo nano /etc/apache2/sites-available/your_domain.conf
```

```bash
<VirtualHost *:80>
ServerName your_domain
ServerAlias www.your_domain
ServerAdmin webmaster@example.com
DocumentRoot /home/ubuntu/django/registration
ErrorLog ${APACHE_LOG_DIR}/django_error.log
CustomLog ${APACHE_LOG_DIR}/django_access.log combined
#Alias /static /home/ubuntu/django/registration/static
#<Directory /home/ubuntu/django/registration/static>
#Require all granted
#</Directory>
#<Directory /home/ubuntu/django/registration/CySm>
#<Files wsgi.py>
#Require all granted
#</Files>
#</Directory>
#WSGIDaemonProcess djangoproj python-path=/home/ubuntu/django/registration python-home=/home/ubuntu/django/mydjangoenv
#WSGIProcessGroup djangoproj
#WSGIScriptAlias / /home/ubuntu/django/registration/CySm/wsgi.py

RewriteEngine on
RewriteCond %{SERVER_NAME} =registration.cybersmarties.in
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

Now we need to uncomment the WSGI lines which we commented during the starting of [this section](#obtaining-an-ssl-certificate) from `/etc/apache2/sites-available/your_domain-le-ssl.conf`. Uncomment the following lines:

```bash
sudo nano /etc/apache2/sites-available/your_domain-le-ssl.conf
```

```bash
...
WSGIDaemonProcess djangoproj python-path=/home/ubuntu/django/registration python-home=/home/ubuntu/django/mydjangoenv
WSGIProcessGroup djangoproj
WSGIScriptAlias / /home/ubuntu/django/registration/CySm/wsgi.py
...
```

Then, run the following command to validate your changes:

```bash
sudo apache2ctl configtest
```

You should get a `Syntax OK` as a response. Restart Apache so that the changes take effect:

```bash
sudo systemctl restart apache2
```

Try reloading your website using `https://` and notice your browser’s security indicator. It should point out that your site is properly secured, typically by including a lock icon 🔒 in the address bar.

You can use the [SSL Labs Server Test](https://www.ssllabs.com/ssltest/) to verify your certificate’s grade and obtain detailed information about it, from the perspective of an external service.

In the next and final step, we’ll test the auto-renewal feature of Certbot, which guarantees that your certificate will be renewed automatically before the expiration date.



## Verifying Certbot Auto-Renewal

Let’s Encrypt’s certificates are only valid for ninety days. This is to encourage users to automate their certificate renewal process, as well as to ensure that misused certificates or stolen keys will expire sooner rather than later.

The Certbot packages on your system come with a cron job or systemd timer that will renew your certificates automatically before they expire. You will not need to run Certbot again, unless you change your configuration.

You can test automatic renewal for your certificates by running this command:

```
sudo certbot renew --dry-run
```

If you see no errors, you’re all set. When necessary, Certbot will renew your certificates and reload Apache to pick up the changes. If the automated renewal process ever fails, Let’s Encrypt will send a message to the email you specified, warning you when your certificate is about to expire.

## Conclusion

If your reading this then you’ve installed the Let’s Encrypt client `certbot`, configured and installed an SSL certificate for your domain, and confirmed that Certbot’s automatic renewal service is active within `systemctl` ✌️. If you have further questions about using Certbot, [their documentation](https://certbot.eff.org/docs/) is a good place to start.

------
