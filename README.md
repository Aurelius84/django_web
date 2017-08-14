# django_web
django_web is a website project based on `Django Admin model`, which helps us tagging corpus manually and easily.
The project is deployed by `Nginx+uwsgi`, it means that you should have already installed `Nginx` on your environment.

`django_web.mysite.mysite_nginx.conf` contains all config information of nginx. You can just copy the content into `/etc/nginx/conf.d/nginx.conf`.

`django_web.mysite.mysite_uwsgi.ini` is the uwsgi ini file. After nginx is already well-configed and service is started, you can run  `uwsgi --ini mysite_uwsgi.ini` to deployed your website.

**Note:** `uwsgi` must be installed correctly. For example no error like this when you install uwsgi `!!! no internal routing support, rebuild with pcre support !!!`


### Requirements
- `Django >= 1.10`
- `PyMySQL`
- `django_smart_selects==1.5.2`
- `python3.5`

### How to use

- **Install virtualenv**
```bash
$ pip install virtualenv

$ git clone the/project/github/url

# cd project
$ cd /your/path/to/project/django_web

# make env using python 3.5
$ virtualenv env --python=python3

# you will see a new dir named “env”; activate the env by followed cmd:
$ source env/bin/activate
```

- **Install requirements via `pip`**

```bash
$ pip install -r requirements.txt
```

- **Nginx and uwsgi**

```bash
# suppose you have installed Nginx and uwsgi
# sudo install nginx
# pip install uwsgi

# nginx
$ cat mysite_nginx.conf >> /etc/nginx/conf.d/nginx.conf
# if there no other www-data web deployed in nginx, you can run:
$ sudo cp mysite_nginx.conf /etc/nginx/conf.d/nginx.conf
# start nginx service
$ sudo /etc/init.d/nginx start

# update your IP in setting.py
$ ifconfig
# copy your machine IP
# update mysit/setting.py ALLOWED_HOSTS like:
# ALLOWED_HOSTS = ['YOUR IP']

# start uwsgi
$ uwsgi --ini mysite_uwsgi.ini
```

- **Visit your website**
```bash
open chrome and visit **http://your_ip:88/admin**
```
### Interface
- **Login**
![Login](https://github.com/KillersDeath/django_web/blob/master/mysite/corpustag/ico.png?raw=true)
- **Corpus tagging**
![tagging](https://github.com/KillersDeath/django_web/blob/master/mysite/corpustag/ico.png?raw=true)
