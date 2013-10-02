import urllib
import sys
import os
import json
from urllib import FancyURLopener
from PIL import Image
import itertools
import optparse
import osaic
import imghdr
import pprint


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        # handle errors the way you'd like to
        # Not going to do anything, just going to skip this file.
        raise Exception("Error downloading image: %s" % errmsg)

def search(term):
    for start in itertools.count():
        query = urllib.urlencode({'q': term, 'rsz': 8, 'start': start * 8, 'imgtype': 'faces', 'as_filetype': 'jpg', 'safe': 'active'})
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&%s' % (query)
        #print url
        search_results = urllib.urlopen(url)
        results = json.loads(search_results.read())
        data = results['responseData']
        if data:
            hits = data['results']
            for h in hits:
                yield (h['url'])
        else:
            raise StopIteration

def showmore(term,num):
    allImages = []
    for i, h in enumerate(itertools.islice(search(term), num)):
        print('{i}: {h}'.format(i=i, h=h))
        allImages.append(h)
    return allImages

def downloadImage(prefix, url, i):
    myopener = MyOpener()
    localFileName = "images/%s-%s.jpg" % (prefix, i)
    try:
        print "D: %s to: %s" % (url, localFileName)
        myopener.retrieve(url, localFileName)
    except Exception, err:
        os.remove(filename)
        sys.stderr.write('ERROR: %s\n' % str(err))
        return None
    return localFileName


def createMosaic(filename, sources, target):
    osaic.mosaicify(
        target=target,
        sources=sources,
        tiles=128,
        zoom=4,
        output=filename,
        )
    print "Success"


if __name__=='__main__':
    # Parse Inputs. Optparse makes it really easy
    parser = optparse.OptionParser()
    parser.add_option("-a", "--action",
                  action="store", type="string", dest="action", help="Specify the action: download or compose")
    parser.add_option("-f", "--file",
                  action="store", type="string", dest="filename", help="The name of the output file")
    parser.add_option("-t", "--target",
                  action="store", type="string", dest="targetfilename", help="The name of the input file to mosaicify")
    parser.add_option("-n", type="int", dest="num", help="How many images to download from Google Images")
    parser.add_option("-q", "--query", action="store", type="string", dest="query", help="Search Term string, ex: automobile")
    parser.add_option("-s", "--sourceDir", action="store", type="string", dest="sourceDir", help="Source Directory, will skip downloading from Google")
    (opts, args) = parser.parse_args()

    outputFileName = "mosaicFinal.jpg" if (opts.filename is None) else opts.filename
    numIterations = 50 if (opts.num is None) else opts.num
    action = "compose"
    if(opts.action is None):
        print "Action argument required"
        parser.print_help()
        exit(-1)
    else:
        action = opts.action.lower()
    if(not (action == "download" or action == "compose")):
        print "Action argument should be either download or compose"
        parser.print_help()
        exit(-1)
    if (action == "download" and opts.query is None):
        print "Query Argument is missing, please specify a search term to query Google images\n"
        parser.print_help()
        exit(-1)
    if (action == "compose" and opts.targetfilename is None):
        print "Target filename is missing, please specify a target image to mosaicify\n"
        parser.print_help()
        exit(-1)

    localImages = []
    if(action == "download"):
        # Retrieve list of images from Google AJAX API Image Search
        urls = showmore(opts.query, numIterations)

        # Download all images and store in /images directory
        for i, image in enumerate(urls):
            filename = downloadImage(opts.query.replace(' ', '-'), image, i)
            try:
                im = Image.open(filename)
                im.verify()
                localImages.append(filename)
            except Exception, err:
                sys.stderr.write('ERROR: %s: %s\n' % (filename, str(err)))

    if(action  == "compose"):
        #Get Images from SourceDIr
        for f in os.listdir(opts.sourceDir):
            filename = os.path.join(opts.sourceDir, f)
            try:
                im = Image.open(filename)
                im.verify()
                localImages.append(filename)
            except Exception, err:
                sys.stderr.write('ERROR: %s: %s\n' % (filename, str(err)))

        # Create Mosaic
        createMosaic(outputFileName, localImages, opts.targetfilename)
