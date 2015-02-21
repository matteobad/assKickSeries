import hashlib
import os
import requests


# Restituisce hash file 
def getHash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


# Scarico english sub (SubDB API)
fileHash = getHash(filePath)
headers = {'User-Agent': 'SubDB/1.0 (assKickSeries/0.1; http://github.com/matteobad/assKickSeries)'}
if requests.get('http://api.thesubdb.com/?action=search&hash='+fileHash, headers=headers):
    response = requests.get('http://api.thesubdb.com/?action=download&hash='+fileHash+'&language=en', headers=headers)
    if response:
        file = open(subPath+'eng.srt', 'wb')
        file.write(response.content)
        file.close()
        print('Sottotitoli inglesi scaricati correttamente')
    else:
        print('Sottotitoli inglesi non trovati')
        return False
