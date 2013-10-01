#Execute these to get a new python virtual environment configured
pip install virtualenv
virtualenv pythonENV
source pythonENV/bin/activate
curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py
easy_install pip
pip install -r ./requirements.txt

