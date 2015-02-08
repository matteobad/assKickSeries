import re
import os
import datetime
import estract


SERIES_URL = 'https://kickass.so/'
SEARCH_URL = 'https://kickass.so/usearch/'


# Scarica tutte le nuove puntate
def newEpisodes(name):
    path = ''.join('serieTV\\'+name.lower()+'.txt')
    file = open(path, 'r+')
    
    while True:
        line = file.readline()
        if line[-2] == 'v' or not line:##
            break
        if compareDate(line) and downloadEpisode(line):
            file.seek(file.tell()-3)
            file.write('v')
            file.seek(file.tell()+2)
            print('Scaricato correttamente')


def compareDate(episode):
    date = re.search(r'[0-9][0-9]-[0-9][0-9]-[0-9]+', episode).group(0)
    if date != '00-00-0000':
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(date, "%d-%m-%Y")    
        if now < date: return False
        else: return True
        
    else:
        return False


# Scarica episodio passato con parametro
def downloadEpisode(episode):
    episode = episode.replace('x', 'e').replace(' ', '-').lower()
    pattern = ''.join('.+e[0-9][0-9]')
    match = re.search(pattern, episode).group(0)
    episode = match[:len(match)-5]+'s'+match[len(match)-5:]

    print('Scarico ->', episode)
    try:
        file = open('hourlydump.txt', encoding='utf8')
        content = file.read()
        pattern = ''.join(SERIES_URL+episode+'.+720p.+x264\S+html')
        torrent = re.search(pattern, content)
        file.close()
        source = estract.estractSource(torrent.group(0))
        magnet = estract.estractMagnet(source)
        os.startfile(magnet)
        return True
    except:
        url = ''.join(SEARCH_URL+episode.replace('-', '%20')+'%20720p%20HDTV%20x264')
        source = estract.estractSource(url)
        if not re.search(r'did not match any documents', source):
            magnet = estract.estractMagnet(source)
            os.startfile(magnet)
            return True
        else:
            print('File non trovato')
            return False
    

# Scarica intera serie TV
def downloadSerie(name):
    path = ''.join('serieTV\\'+name.lower()+'.txt')
    file = open(path, 'r')
    content = file.readlines()
    for episode in content:
        downloadEpisode(episode)


# Scarica ogni puntata di ogni serie
def downloadAll():
    file = open('preferiti.txt', 'r')
    content = file.readlines()
    for serie in content:
        downloadSerie(serie)
