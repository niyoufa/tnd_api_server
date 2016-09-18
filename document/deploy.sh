#!/bin/sh
cd /usr/share/nginx/dhuicredit
git pull origin dev
supervisorctl restart all