mosaic
======

Downloads Images from Google Image Search and creates a mosaic

To install, on a Mac OSX Lion, make sure to have installed JPEG support:
$ curl -O http://www.ijg.org/files/jpegsrc.v8c.tar.gz
$ tar zxvf jpegsrc.v8c.tar.gz
$ cd jpeg-8c/
$ ./configure
$ make
$ sudo make install

Then simply run python setup.py, this will install all neccessary requirements.

To execute, simply run python mosaic.py -query "automobile" -n 50 -targetImage "yourphoto.jpg" -f "outputfile.jpg"

