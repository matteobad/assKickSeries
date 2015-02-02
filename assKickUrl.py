import urllib.request, zlib, gzip, os

apiURL = 'https://kickass.so/hourlydump.txt.gz'

# Aggiorna file API
def updateAPI():
    urllib.request.urlretrieve(apiURL, 'hourlydump.txt.gz')
    _gzipData = gzip.GzipFile('hourlydump.txt.gz', 'rb')
    _data = _gzipData.read()
    _gzipData.close()

    _file = open('hourlydump.txt','wb')
    _file.write(_data)
    _file.close()
        
    os.remove('hourlydump.txt.gz')

# Restituisce HTML source dell'url in input
def HTMLsource(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0'),
                         ('Accept-Encoding', 'gzip,deflate')]
    
    page = opener.open(url)
    encoding = page.info().get("Content-Encoding")
    content = page.read()
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        source = zlib.decompress(content, 16+zlib.MAX_WBITS)
        result = source.decode('utf-8')
    else:
        result = page.read()
    page.close()

    return result
