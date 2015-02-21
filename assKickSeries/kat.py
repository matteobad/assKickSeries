#######################################################
#                                                     #
#  Modulo per estrarre dati da kickAssTorrent naviga  #
#  all'interno del sito per reperire le informazioni  #
#  ed i dati necessari al funzionamento dello script  #
#  dello script.                                      #
#  Necessarie le librerie esterne: requests, lxml     #
#                                                     #      
#######################################################

import setup
import re
import os
import zlib
import requests
import lxml.html
import datetime



MONTHS = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
          'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
          'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

NUMBER = ['00','01','02','03','04','05','06','07','08','09',
          '10','11','12','13','14','15','16','17','18','19',
          '20','21','22','23','24','25','26','27','28','29',]



# Restituisce HTML source dell'url in input
def getSource(url):
    headers = {'User-Agent': 'AssKickSeries 0.1',
               'Accept-Encoding': 'gzip'}
    source = requests.get(url, headers=headers).text
    return source


# Aggiorna file API
def getHourlydump():
    response = requests.get('http://kat.ph/hourlydump.txt.gz')
    data = zlib.decompress(response.content, zlib.MAX_WBITS | 16)

    with open('hourlydump.txt', 'wb') as file:
        file.write(data)
        file.close()


# Cerca nome serie TV (<h1> kat.ph)
def getShowName(source):
    tree = lxml.html.fromstring(source)
    try: return tree.xpath('//h1/text()')[0]
    except: return False


# Restituisce [00x00 titolo; data, ...]
def getEpisodes(source):
    tree = lxml.html.fromstring(source)
    divs = tree.xpath('//div[@class="infoListCut"]')
    
    index = getSeasons(source)
    precEp = '100'
    result = []
    for div in divs:
        div = lxml.html.tostring(div).decode('utf-8')
        episode = re.search(r'Episode [0-9]+', div).group(0).replace('Episode ', '')
        title = re.search(r'Name">.+<', div).group(0).replace('Name">', '').replace('<', '')
        date = getDate(re.search(r'Date">.+[0-9][0-9][0-9][0-9]', div))
        if int(episode) > int(precEp):
            index -= 1
        season = NUMBER[index]
        precEp = episode
        
        result.append(''.join(season+'x'+episode+' '+title+'; '+date))
    return result


# Cerca numero stagioni
def getSeasons(source):
    tree = lxml.html.fromstring(source)
    try: return int(tree.xpath('//h3/text()')[0].replace('Season ', ''))
    except: return False


# Cerca data di uscita episodio
def getDate(rawDate):
    try:
        date = rawDate.group(0)[-11:]
        day = date[4:6].replace(' ', '0')
        month = MONTHS.get(date[:3])
        year = date[7:]
        return day+'-'+month+'-'+year
    
    except:
        return '00-00-0000'


# Cerca l'url della pagina della serie TV
def getShowPage(name):
    for i in range(1, 10):
        url = 'http://kat.ph/usearch/'+name.replace(' ', '%20')+'%20s0'+str(i)+'e01'
        source = getSource(url)
        try:
            match = re.search(r'/\S+tv[0-9]+', source).group(0)
            return 'http://kat.ph'+match
        except:
            pass


# Cerca magnet link
def getMagnet(source):
    match = re.search(r'magnet:\S+\b', source)
    return match.group(0) if match else False


# Scarica tutte le nuove puntate
def downloadNewEpisodes(name):
    path = 'serieTV\\'+name+'.txt'
    with open(path, 'r+') as file:  
        while True:
            line = file.readline()
            if line[-2] == 'v' or not line:
                break
            # Scarica e contrassegna episodio
            if compareDate(line) and downloadEpisode(line):
                file.seek(file.tell()-3)
                file.write('v')
                file.seek(file.tell()+2)
                print('Scaricato correttamente')


# Compara due date 
def compareDate(episode):
    date = re.search(r'[0-9][0-9]-[0-9][0-9]-[0-9]+', episode).group(0)
    if date != '00-00-0000':
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(date, "%d-%m-%Y")    
        if now <= date: return False
        else: return True
        
    else:
        return False


# Scarica episodio passato con parametro
def downloadEpisode(episode):
    episode = episode.replace(' ', '-')
    match = re.search(r'.+x[0-9][0-9]', episode).group(0)
    episode = match[:len(match)-5]+'s'+match[len(match)-5:].replace('x', 'e')

    quality = setup.getSetting('quality')

    print('Scarico ->', episode)
    try:
        # Cerco file in hourlydump.txt (KickAss API)
        with open('hourlydump.txt', encoding='utf8') as file:
            content = file.read()
            file.close()
        
        pattern = ''.join('http://kat.ph/'+episode+'.+'+quality+'.+x264\S+html')
        torrent = re.search(pattern, content)
        source = getSource(torrent.group(0))
        magnet = getMagnet(source)
        os.startfile(magnet)
        return True
    
    except:
        # Se non lo trovo cerco online
        episode = episode.replace('-', '%20')
        url = ''.join('http://kat.ph/usearch/'+episode+'%20'+quality+'%20HDTV%20x264')
        source = getSource(url)
        if not re.search(r'did not match any documents', source):
            magnet = getMagnet(source)
            os.startfile(magnet)
            return True
        else:
            print('File non trovato')
            return False
    

# Scarica intera serie TV
def downloadSingleShow(name):
    path = ''.join('serieTV\\'+name+'.txt')
    with open(path, 'r') as file:
        content = file.readlines()
        file.close()
    for episode in content:
        downloadEpisode(episode)


# Scarica ogni puntata di ogni serie
def downloadAllShows():
    with open('preferiti.txt', 'r') as file:
        content = file.readlines()
        file.close()
    for serie in content:
        downloadSerie(serie)
