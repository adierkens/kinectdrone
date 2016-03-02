rm -rf env
virtualenv -p /usr/local/bin/python2.7 --no-site-packages env

./env/bin/pip install -r requirements.txt

