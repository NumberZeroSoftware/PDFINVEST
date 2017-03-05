mkdir ocropy
cd ocropy
git clone https://github.com/tmbdev/ocropy.git
sudo apt-get install $(cat PACKAGES)
wget -nd http://www.tmbdev.net/en-default.pyrnn.gz
mv en-default.pyrnn.gz models/
sudo python setup.py install
cd ..
./update_ocropy.sh
sudo cp Ocropy_Modificado/chars.py  /usr/local/lib/python2.7/dist-packages/ocrolib
sudo cp Ocropy_Modificado/PDFINVEST6.pyrnn.gz /usr/local/share/ocropus/
# Need the git clone of the ocropy repo
# Must be inside ocropy folder