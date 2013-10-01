import urllib
import sys
import json
from urllib import FancyURLopener
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
        print "Downloading: %s to: %s" % (url, localFileName)
        myopener.retrieve(url, localFileName)
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return None
    if (imghdr.what('jpg', localFileName)):
        print "Image %s isn't valid" % localFileName
        return None
    print localFileName
    return localFileName


def createMosaic(filename, sources, target):
    osaic.mosaicify(
        target=target,
        sources=sources,
        tiles=128,
        zoom=4,
        output=filename,
        )


if __name__=='__main__':
    # Parse Inputs. Optparse makes it really easy
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file",
                  action="store", type="string", dest="filename", help="The name of the output file")
    parser.add_option("-n", type="int", dest="num", help="How many images to download from Google Images")
    parser.add_option("-q", "--query", action="store", type="string", dest="query", help="Search Term string, ex: automobile")
    (opts, args) = parser.parse_args()

    outputFileName = "mosaicFinal.jpg" if (opts.filename is None) else opts.filename
    numIterations = 50 if (opts.num is None) else opts.num

    if (opts.query is None):
        print "Query Argument is missing, please specify a search term to query Google images\n"
        parser.print_help()
        exit(-1)

    # Retrieve list of images from Google AJAX API Image Search
    urls = showmore(opts.query, numIterations)

    # Download all images and store in /images directory
    localImages = []
    for i, image in enumerate(urls):
        localImages.append(downloadImage(opts.query.replace(' ', '-'), image, i))

    # Create Mosaic
    createMosaic(outputFileName, localImages, 'images/bicycle-3.jpg')
