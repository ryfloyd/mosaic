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

To execute, two different executions of the script are required, first download a set of images to be the tiles in the mosaic:
  python mosaic.py -a "download" -q "automobile" -n 50 
Next, execute with --action compose to create the Mosaic using the targetfile as the template
  python mosaic.py -a "compose" -t yourphoto.jpg -f outputfile.jpg -s ./images
