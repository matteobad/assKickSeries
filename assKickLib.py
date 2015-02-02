import string, re, os
import assKickTime, assKickUrl

episode = ['00','01','02','03','04','05','06','07','08','09',
           '10','11','12','13','14','15','16','17','18','19',
           '20','21','22','23','24','25','26','27','28','29',]

season = ['00','01','02','03','04','05','06','07','08','09',
           '10','11','12','13','14','15','16','17','18','19']

searchURL = 'https://kickass.so/usearch/'
seriesURL = 'https://kickass.so/'

# Cerca pagina serie TV su kickAss
def findSeriePage(name):
    print('Cerco serie TV...')
    for i in range(1,6):
        url = ''.join(searchURL+name.replace(' ', '%20')+'%20s'+season[i]+'e01%20720p')
        print(url)
        source = assKickUrl.HTMLsource(url)
        serieNumber = re.search(name.replace(' ', '-')+'-tv[0-9]+', source)
        if serieNumber:
            seriePage = ''.join(seriesURL+serieNumber.group(0))
            return seriePage
    return False


# Crea file serie TV
def updateSerieFile(name, url):
    source = assKickUrl.HTMLsource(url)

    #creo lista episodi episodi
    episodes = re.findall(r'\b[0-9][0-9]\t', source)
    episodes = [ep.replace('\t', '') for ep in episodes]
    
    #determino stagioni
    seasons = re.search(r'Season [0-9][0-9]', source).group(0).replace('Season ', '')
    if len(seasons) == 2: i = int(seasons)
    else: i = int(seasons[1])

    #determino lista titoli
    rawTitles = re.findall(r'versionsEpName">[^<]+', source)
    titles = [element.replace('versionsEpName">', '') for element in rawTitles]

    #determino data rilascio
    rawDate = re.findall(r'versionsEpDate">.+[0-9]+', source)
    rawDate = [element.replace('versionsEpDate">', '') for element in rawDate]
    date = assKickTime.dateConvert(rawDate, len(episodes))

    #scrivo su file
    file = open(''.join('serieTV//'+name+'.txt'), 'w')
    check = 'x'
    for j in range(len(episodes)):
        if assKickTime.compareDate(date[j]): check = 'v'
        else: check = 'x'
        stringFile = ''.join(name.title()+' '+season[i]+'x'+episodes[j]+' '+titles[j]+'; '+date[j]+check+'\n')
        if episodes[j] == '01':
            i -= 1
        file.write(stringFile)
    file.close()


# Scarica episodio da stringa
def downloadEpisode(rawString):
    rawSearch = re.search(r'.+x[0-9][0-9]', rawString).group(0).replace('x', 'e').replace(' ', '-').lower()
    search = rawSearch[:len(rawSearch)-5]+'s'+rawSearch[len(rawSearch)-5:]
    
    _file = open('hourlydump.txt', encoding='utf8')
    hourlydump = _file.read()
    torrent = re.search(seriesURL+search+'-720p-hdtv-x264\S+html', hourlydump)
    _file.close()
    if torrent:
        print('Scarico -> ', search)
        source = assKickUrl.HTMLsource(torrent.group(0))
        magnetLink = re.search(r'magnet:\S+\b', source).group(0)
        os.startfile(magnetLink)
    else:
        print('File non trovato')

