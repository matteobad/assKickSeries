import string
import re
import requests
import lxml.html


MONTHS = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
          'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
          'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

NUMBER = ['00','01','02','03','04','05','06','07','08','09',
          '10','11','12','13','14','15','16','17','18','19',
          '20','21','22','23','24','25','26','27','28','29',]

SEARCH_URL = 'https://kickass.so/usearch/'
SERIES_URL = 'https://kickass.so'


# Restituisce HTML source dell'url in input
def estractSource(url):
    source = requests.get(url, verify=True).text
    return source


# Restituisce nome serie TV o False
def estractName(source):
    tree = lxml.html.fromstring(source)
    try: return tree.xpath('//h1/text()')[0]
    except: return False


# Restituisce [00x00 titolo; data, ...]
def estractEpisodes(source):
    tree = lxml.html.fromstring(source)
    divs = tree.xpath('//div[@class="infoListCut"]')
    
    index = estractSeasons(source)
    precEp = '100'
    result = []
    for div in divs:
        div = lxml.html.tostring(div).decode('utf-8')
        episode = re.search(r'Episode [0-9]+', div).group(0).replace('Episode ', '')
        title = re.search(r'Name">.+<', div).group(0).replace('Name">', '').replace('<', '')
        date = estractDate(re.search(r'Date">.+[0-9][0-9][0-9][0-9]', div))
        if int(episode) > int(precEp):
            index -= 1
        season = NUMBER[index]
        precEp = episode
        
        result.append(''.join(season+'x'+episode+' '+title+'; '+date))
    return result


# Resituisce indice stagione
def estractSeasons(source):
    tree = lxml.html.fromstring(source)
    try: return int(tree.xpath('//h3/text()')[0].replace('Season ', ''))
    except: return False
    

# Restituisce data uscita episodio
def estractDate(rawDate):
    if rawDate:
        date = rawDate.group(0)[-11:]
        day = date[4:6].replace(' ', '0')
        month = MONTHS.get(date[:3])
        year = date[7:]
        return ''.join(day+'-'+month+'-'+year)
    else:
        return '00-00-0000'


# Cerca l'url della serie TV
def estractPage(name):
    pattern = ''.join(r'/\S+tv[0-9]+')
    for i in range(1, 10):
        url = ''.join(SEARCH_URL+name.replace(' ', '%20')+'%20s0'+str(i)+'e01')
        source = estractSource(url)
        match = re.search(pattern, source)
        if match:
            return ''.join(SERIES_URL+match.group(0))
    return False


# Cerca magnet link
def estractMagnet(source):
    pattern = ''.join(r'magnet:\S+\b')
    match = re.search(pattern, source)
    if match:
        return match.group(0)
    else:
        return False
