sudo apt-get install $(cat PACKAGES)
wget -nd http://www.tmbdev.net/en-default.pyrnn.gz
mv en-default.pyrnn.gz models/
sudo python setup.py install
# Need the git clone of the ocropy repo
# Must be inside ocropy folder