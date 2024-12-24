

import urllib2

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    f = open("the_downloaded_file.pdf", 'wb')
    f.write(response.read())
    f.close()

download_file("some url to pdf here")
