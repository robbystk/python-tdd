Provisioning a new site
=======================

## Required Packages:
- nginx
- python3
- virtualenv & pip
- git

e.g. on Ubuntu:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install nginx git python3 python3-venv
```

## Nginx Virtual Host Config
- see nginx.template.conf
- replace `DOMAIN` with e.g., `staging.my-domain.com`

## Systemd service
- see gunicort-systemd.template.service
- replace `DOMAIN` with e.g., `staging.my-domain.com`

## Directory Structure
Assume we have a user account at /home/username/
```
/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
```
