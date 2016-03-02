rm -rf env
virtualenv -p /usr/local/bin/python2.7 --no-site-packages env

./env/bin/pip install -r requirements.txt

echo "/usr/local/opt/opencv3/lib/python2.7/site-packages" > ./env/lib/python2.7/site-packages/opencv3.pth


