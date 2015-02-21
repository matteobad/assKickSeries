#########################################################
#                                                       #
#  Modulo per accedere alle API di itasa e scaricare    #
#  sottotitoli o trovare informazioni varie riguardo    #
#  serie TV, utenti, news, sottotitoli...               #
#  Possibilità di accedere ai contenuti myItasa. Per    #
#  maggiori informazioni leggere doc:                   #
#                                                       #
#  https://api.italiansubs.net/docs.pdf                 #
#                                                       #
#########################################################

import setup
import os
import re
import requests
import html
import zipfile
from xml.dom import minidom



URL = 'https://api.italiansubs.net/api/rest/'
APIKEY = '67f463eae6e14828b64da78fe40ebcb5'

Category = {'16':'Serie TV',
            '27':'Anime',
            '28':'Film',
            '30':'Documentari',
            '31':'Speciali'}

version = ['normale', '1080i', '1080p', '720p', 'bdrip',
           'bluray', 'dvdrip', 'hdtv', 'hr', 'web-dl']



# Restituisce HTML source dell'url in input
def getSource(url):
    headers = {'User-Agent': 'AssKickSeries 0.1'}
    source = requests.get(url, headers=headers).text
    return source


# Cerca tutte le news
def getNewsList():
    url = URL+'news?&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        news = xmldoc.getElementsByTagName('news')
        for element in news:
            newsId = element.getElementsByTagName('id')[0].firstChild.data
            showId = element.getElementsByTagName('show_id')[0].firstChild.data
            showName = element.getElementsByTagName('show_name')[0].firstChild.data
            special = element.getElementsByTagName('special')[0].firstChild.data
            category = element.getElementsByTagName('category')[0].firstChild.data
            image = element.getElementsByTagName('image')[0].firstChild.data
            imageBy = element.getElementsByTagName('image_by')[0].firstChild.data
            team = element.getElementsByTagName('team')[0].firstChild.data
            submitDate = element.getElementsByTagName('submit_date')[0].firstChild.data
            submitBy = element.getElementsByTagName('submitted_by')[0].firstChild.data
            thumb = element.getElementsByTagName('thumb')[0].firstChild.data
            episode = element.getElementsByTagName('episode')[0].firstChild.data

        page = xmldoc.getElementsByTagName('page')[0].firstChild.data
        pages = xmldoc.getElementsByTagName('pages')[0].firstChild.data
        count = element.getElementsByTagName('count')[0].firstChild.data
        nextPage = element.getElementsByTagName('next')[0].firstChild.data
    else:
        print('Errore nella lettura delle news')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca dettagli per una singola news
def getNewsDetail(newsId):
    url = URL+'news/'+newsId+'?apikey='+APIKEY
    source =getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        news = xmldoc.getElementsByTagName('news')
        
        showId = news.getElementsByTagName('show_id')[0].firstChild.data
        showName = news.getElementsByTagName('show_name')[0].firstChild.data
        special = news.getElementsByTagName('special')[0].firstChild.data
        category = news.getElementsByTagName('category')[0].firstChild.data
        translation = news.getElementsByTagName('translation')[0].firstChild.data
        sync = news.getElementsByTagName('sync')[0].firstChild.data
        resync = news.getElementsByTagName('resync')[0].firstChild.data
        info = html.unescape(news.getElementsByTagName('info')[0].firstChild.data)
        image = news.getElementsByTagName('image')[0].firstChild.data
        imageBy = news.getElementsByTagName('image_by')[0].firstChild.data
        team = news.getElementsByTagName('team')[0].firstChild.data
        submitDate = news.getElementsByTagName('submit_date')[0].firstChild.data
        
        subtitles = news.getElementsByTagName('subtitle')
        for sub in subtitles:
            subId = sub.getElementsByTagName('subtitle')[0].firstChild.data
            name = sub.getElementsByTagName('name')[0].firstChild.data
            version = news.getElementsByTagName('version')[0].firstChild.data
            
        submitBy = news.getElementsByTagName('submitted_by')[0].firstChild.data
        episode = news.getElementsByTagName('episode')[0].firstChild.data
        thumb = news.getElementsByTagName('thumb')[0].firstChild.data
    else:
        print('Errore nella lettura della news')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca news per una serie TV
def getNewsFor(showName, page='1'):
    url = URL+'news/search?q='+showName+'&page='+page+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        news = xmldoc.getElementsByTagName('news')
        for element in news:
            newsId = element.getElementsByTagName('id')[0].firstChild.data
            showId = element.getElementsByTagName('show_id')[0].firstChild.data
            showName = element.getElementsByTagName('show_name')[0].firstChild.data
            special = element.getElementsByTagName('special')[0].firstChild.data
            category = element.getElementsByTagName('category')[0].firstChild.data
            image = element.getElementsByTagName('image')[0].firstChild.data
            imageBy = element.getElementsByTagName('image_by')[0].firstChild.data
            team = element.getElementsByTagName('team')[0].firstChild.data
            submitDate = element.getElementsByTagName('submit_date')[0].firstChild.data
            submitBy = element.getElementsByTagName('submitted_by')[0].firstChild.data
            thumb = element.getElementsByTagName('thumb')[0].firstChild.data
            
        page = xmldoc.getElementsByTagName('page')[0].firstChild.data
        pages = xmldoc.getElementsByTagName('pages')[0].firstChild.data
        count = xmldoc.getElementsByTagName('count')[0].firstChild.data
        nextPage = xmldoc.getElementsByTagName('next')[0].firstChild.data
    else:
        print('Errore nella lettura delle news per', showName)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)
        

# Cerca lista completa serie TV
def getShowsList():
    url = URL+'shows?apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        shows = xmldoc.getElementsByTagName('show')
        for element in shows:
            showId = element.getElementsByTagName('id')[0].firstChild.data
            showName = element.getElementsByTagName('name')[0].firstChild.data
            fans = element.getElementsByTagName('fans')[0].firstChild.data
    else:
        print('Errore nella lettura delle serie TV')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca dettagli serie TV
def getShowDetails(showId):
    url = URL+'shows/'+showId+'?apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getelementsByTagName('status')[1].firstChild.data
    if status == 'success':
        show = xmldoc.getElementsByTagName('show')

        showName = show.getElementsByTagName('name')[0].firstChild.data
        tvdbId = show.getElementsByTagName('id_tvdb')[0].firstChild.data
        tvrageId = show.getElementsByTagName('id_tvrage')[0].firstChild.data
        tvdbName = show.getElementsByTagName('name_tvdb')[0].firstChild.data
        tvrageName = show.getElementsByTagName('name_tvrage')[0].firstChild.data
        plot = show.getElementsByTagName('plot')[0].firstChild.data
        plotLang = show.getElementsByTagName('plot_lang')[0].firstChild.data
        banner = show.getElementsByTagName('banner')[0].firstChild.data
        lastUpdate = show.getElementsByTagName('last_update')[0].firstChild.data
        folderThumb = show.getElementsByTagName('folder_thumb')[0].firstChild.data
        
        actors = show.getElementsByTagName('actor')
        for element in actors:
            name = element.getElementsByTagName('name')[0].firstChild.data
            iterprets = element.getElementsByTagName('as')[0].firstChild.data
            image = element.getElementsByTagName('image')[0].firstChild.data

        genres = show.getElementsByTagName('genre')
        for element in genres:
            genre = element[0].firstChild.data

        started = show.getElementsByTagName('started')[0].firstChild.data
        ended = show.getElementsByTagName('ended')[0].firstChild.data
        seasons = show.getElementsByTagName('seasons')[0].firstChild.data
        classification = show.getElementsByTagName('classification')[0].firstChild.data
        country = show.getElementsByTagName('country')[0].firstChild.data
        status = show.getElementsByTagName('status')[0].firstChild.data
        network = show.getElementsByTagName('network')[0].firstChild.data
        runtime = show.getElementsByTagName('runtime')[0].firstChild.data
        airday = show.getElementsByTagName('airday')[0].firstChild.data
        airtime = show.getElementsByTagName('airtime')[0].firstChild.data
        lastEpNumber = show.getElementsByTagName('lastep_num')[0].firstChild.data
        lastEpTitle = show.getElementsByTagName('lastep_title')[0].firstChild.data
        lastEpDate = show.getElementsByTagName('lastep_date')[0].firstChild.data
        nextEpNumber = show.getElementsByTagName('nextep_num')[0].firstChild.data
        nextEpTitle = show.getElementsByTagName('nextep_title')[0].firstChild.data
        nextEpDate = show.getElementsByTagName('nextep_date')[0].firstChild.data
        fans = show.getElementsByTagName('fans')[0].firstChild.data
    else:
        print('Errore nella lettura dei dettagli di', showId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca prossimi episodi
def getNextEpisodes():
    url = URL+'shows/nextepisodes?apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getelementsByTagName('status')[0].firstChild.data
    if status == 'success':
        shows = xmldoc.getElementsByTagName('show')
        for element in shows:
            showId = element.getElementsByTagName('id')[0].firstChild.data
            showName = element.getElementsByTagName('name')[0].firstChild.data
            folderThumb = element.getElementsByTagName('folder_thumb')[0].firstChild.data
            country = element.getElementsByTagName('country')[0].firstChild.data
            network = element.getElementsByTagName('network')[0].firstChild.data
            runtime = element.getElementsByTagName('runtime')[0].firstChild.data
            airtime = element.getElementsByTagName('airtime')[0].firstChild.data
            nextEpNumber = element.getElementsByTagName('nextep_num')[0].firstChild.data
            nextEpTitle = element.getElementsByTagName('nextep_title')[0].firstChild.data
            nextEpDate = element.getElementsByTagName('nextep_date')[0].firstChild.data
    else:
        print('Errore nella lettura dei prossimi episodi')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca immagine cartella per serie TV
def getFolderImage(showId):
    url = URL+'shows/'+showId+'/folderThumb?apikey='+APIKEY
    headers = {'User-Agent':'AssKickSeries 0.1'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        with open('serieTV\\image\\'+showId+'.png', 'wb') as file:
            file.write(response.content)
            file.close()
    else:
        response = requests.get('http://www.italiansubs.net/varie/ico/unknown.png', headers=headers)
        with open('serieTV\\image\\'+showId+'.png', 'wb') as file:
            file.write(response.content)
            file.close()


# Cerca serie TV
def getShowsBySearch(keyword, page='1'):
    url = URL+'shows/search?q='+keyword+'&page='+page+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        shows = xmldoc.getElementsByTagName('show')
        for element in shows:
            showId = element.getElementsByTagName('id')[0].firstChild.data
            #showName = element.getElementsByTagName('name')[0].firstChild.data
            return showId
    else:
        print('Errore nella ricerca delle serie TV')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca sottotitoli di una serie TV
def getShowSubs(showId, version='720p', page='1'):
    url = URL+'subtitles?show_id='+showId+'&version='+version+'&page='+page+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        subtitles = xmldoc.getElementsByTagName('subtitle')
        for element in subtitles:
            subId = element.getElementsByTagName('id')[0].firstChild.data
            subName = element.getElementsByTagName('name')[0].firstChild.data
            subVersion = element.getElementsByTagName('version')[0].firstChild.data

        page = xmldoc.getElementsByTagName('page')[0].firstChild.data
        pages = xmldoc.getElementsByTagName('pages')[0].firstChild.data
        count = xmldoc.getElementsByTagName('count')[0].firstChild.data
        nextPage = xmldoc.getElementsByTagName('next')[0].firstChild.data
    else:
        print('Errore nella ricerca di sub', version, 'per', showId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca dettagli sottotitolo
def getSubDetails(subId):
    url = URL+'subtitles/'+subId+'?apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        subtitle = xmldoc.getElementsByTagName('subtitle')

        subName = element.getElementsByTagName('name')[0].firstChild.data
        subVersion = element.getElementsByTagName('version')[0].firstChild.data
        fileName = element.getElementsByTagName('filename')[0].firstChild.data
        fileSize = element.getElementsByTagName('filesize')[0].firstChild.data
        fileTypes = element.getElementsByTagName('filetypes')[0].firstChild.data
        desc = html.unescape(element.getElementsByTagName('description')[0].firstChild.data)
        downloads = element.getElementsByTagName('downloads')[0].firstChild.data
        submitDate = element.getElementsByTagName('submit_date')[0].firstChild.data
        showId = element.getElementsByTagName('show_id')[0].firstChild.data
        showName = element.getElementsByTagName('show_name')[0].firstChild.data
        submittedBy = element.getElementsByTagName('submitted_by')[0].firstChild.data
    else:
        print('Errore nella ricerca di sub', version, 'per', showId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca sottotitoli
def getSubtitle(keyword='', version='720p', page='1', showId=''):
    url = URL+'subtitles/search?q='+keyword+'&version='+version+'&page='+page+'&show_id='+showId+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        subtitles = xmldoc.getElementsByTagName('subtitle')
        for element in subtitles:
            try:
                subId = element.getElementsByTagName('id')[0].firstChild.data
                subName = element.getElementsByTagName('name')[0].firstChild.data
                return subId
            except:
                return False
            #subVersion = element.getElementsByTagName('version')[0].firstChild.data
            #showId = element.getElementsByTagName('show_id')[0].firstChild.data
            #showName = element.getElementsByTagName('show_name')[0].firstChild.data

        #page = xmldoc.getElementsByTagName('page')[0].firstChild.data
        #pages = xmldoc.getElementsByTagName('pages')[0].firstChild.data
        #count = xmldoc.getElementsByTagName('count')[0].firstChild.data
        #nextPage = xmldoc.getElementsByTagName('next')[0].firstChild.data
        return False
    else:
        print('Errore nella ricerca di', keyword, version, 'per', showId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)
    

# Login
def itasaLogin():
    with open('impostazioni.txt', 'r') as file:
        content = file.read()
        file.close()

    user = setup.getSetting('itasaUser')
    passwd = setup.getSetting('itasaPass')
    if not user or not passwd:
        user = input('Username Itasa: -> ')
        passwd = input('Password Itasa: -> ')

        newContent = content+'\nitasaUser='+user+'\nitasaPass='+passwd
        with open('impostazioni.txt', 'w') as file:
            content = file.write(newContent)
            file.close()
        
    url = URL+'users/login?username='+user+'&password='+passwd+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        #userId = xmldoc.getElementsByTagName('id')[0].firstChild.data
        #name = xmldoc.getElementsByTagName('name')[0].firstChild.data
        #username = xmldoc.getElementsByTagName('username')[0].firstChild.data
        #email = xmldoc.getElementsByTagName('email')[0].firstChild.data
        #lastVisit = xmldoc.getElementsByTagName('last_visit')[0].firstChild.data
        authcode = xmldoc.getElementsByTagName('authcode')[0].firstChild.data
        #hasMyItasa = xmldoc.getElementsByTagName('has_myitasa')[0].firstChild.data
        #registerDate = xmldoc.getElementsByTagName('register_date')[0].firstChild.data
        #gender = xmldoc.getElementsByTagName('gender')[0].firstChild.data
        #birthdate = xmldoc.getElementsByTagName('birthdate')[0].firstChild.data
        #location = xmldoc.getElementsByTagName('location')[0].firstChild.data
        #website = xmldoc.getElementsByTagName('website_url')[0].firstChild.data
        #unreadMessages = xmldoc.getElementsByTagName('unread_message')[0].firstChild.data
        #karmaBad = xmldoc.getElementsByTagName('karma_bad')[0].firstChild.data
        #karmaGood = xmldoc.getElementsByTagName('karma_good')[0].firstChild.data
        return authcode
    else:
        print('Errore nel login')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca profilo utente da user ID
def getUserProfile(userId=''):
    authcode = itasaLogin()
    url = URL+'users/'+userId+'?authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        #userId = xmldoc.getElementsByTagName('id')[0].firstChild.data
        #name = xmldoc.getElementsByTagName('name')[0].firstChild.data
        #username = xmldoc.getElementsByTagName('username')[0].firstChild.data
        #email = xmldoc.getElementsByTagName('email')[0].firstChild.data
        #lastVisit = xmldoc.getElementsByTagName('last_visit')[0].firstChild.data
        #authcode = xmldoc.getElementsByTagName('authcode')[0].firstChild.data
        hasMyItasa = xmldoc.getElementsByTagName('has_myitasa')[0].firstChild.data
        #registerDate = xmldoc.getElementsByTagName('register_date')[0].firstChild.data
        #gender = xmldoc.getElementsByTagName('gender')[0].firstChild.data
        #birthdate = xmldoc.getElementsByTagName('birthdate')[0].firstChild.data
        #location = xmldoc.getElementsByTagName('location')[0].firstChild.data
        #website = xmldoc.getElementsByTagName('website_url')[0].firstChild.data
        #unreadMessages = xmldoc.getElementsByTagName('unread_message')[0].firstChild.data
        #avatar = xmldoc.getElementsByTagName('avatar')[0].firstChild.data
        #karmaBad = xmldoc.getElementsByTagName('karma_bad')[0].firstChild.data
        #karmaGood = xmldoc.getElementsByTagName('karma_good')[0].firstChild.data
        return hasMyItasa
    else:
        print('Errore nella ricerca di', userId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca lista serie TV preferite
def getFavouriteShows():
    authcode = itasaLogin()
    url = URL+'myitasa/shows?authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        if getUserProfile() == '1':
            shows = xmldoc.getElementsByTagName('show')
            result = []
            for element in shows:
                showId = element.getElementsByTagName('id')[0].firstChild.data
                showName = element.getElementsByTagName('name')[0].firstChild.data
                #versions = element.getElementsByTagName('version')
                #for element in versions:
                #    version = element[0].firstChild.data
                result.append(showId+';'+showName)
            return result
        else:
            print('MyItasa non attivo')
    else:
        print('Errore nella ricerca di', keyword, version, 'per', showId)
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca ultimi sottotitoli preferiti
def getLastSubs(page='1'):
    authcode = itasaLogin()
    url = URL+'myitasa/lastsubtitles?page='+page+'&authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        if getUserProfile() == '1':
            subtitles = xmldoc.getElementsByTagName('subtitle')
            for element in subtitles:
                subId = element.getElementsByTagName('id')[0].firstChild.data
                subName = element.getElementsByTagName('name')[0].firstChild.data
                version = element.getElementsByTagName('version')[0].firstChild.data
                submitDate = element.getElementsByTagName('submit_date')[0].firstChild.data
                showId = element.getElementsByTagName('show_id')[0].firstChild.data
                downloadDate = element.getElementsByTagName('download_date')[0].firstChild.data
            page = xmldoc.getElementsByTagName('page')[0].firstChild.data
            pages = xmldoc.getElementsByTagName('pages')[0].firstChild.data
            count = element.getElementsByTagName('count')[0].firstChild.data
            nextPage = element.getElementsByTagName('next')[0].firstChild.data
        else:
            print('MyItasa non attivo')
    else:
        print('Errore nella ricerca dei sub preferiti')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Cerca prossimi episodi preferiti
def getNextEpisodes(page='1'):
    authcode = itasaLogin()
    url = URL+'myitasa/nextepisodes?page='+page+'&authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        if getUserProfile() == '1':
            episodes = xmldoc.getElementsByTagName('episode')
            for element in subtitles:
                showId = element.getElementsByTagName('show_id')[0].firstChild.data
                showName = element.getElementsByTagName('show_name')[0].firstChild.data
                number = element.getElementsByTagName('number')[0].firstChild.data
                title = element.getElementsByTagName('title')[0].firstChild.data
                date = element.getElementsByTagName('date')[0].firstChild.data
        else:
            print('MyItasa non attivo')
    else:
        print('Errore nella ricerca dei prossimi episodi')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Aggiunge serie TV ai preferiti
def addToMyItasa(showId, version='720p'):
    authcode = itasaLogin()
    url = URL+'myitasa/addShowToPref?show_id='+showId+'&version='+version+'&authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        if getUserProfile() == '1':
            pass
            #getFavouriteShows()
        else:
            print('MyItasa non attivo')
    else:
        print('Errore nella ricerca dei prossimi episodi')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Rimuove serie TV dai preferiti
def removeFromMyItasa(showId, version=''):
    authcode = itasaLogin()
    url = URL+'myitasa/removeShowFromPref?show_id='+showId+'&version='+version+'&authcode='+authcode+'&apikey='+APIKEY
    source = getSource(url)

    xmldoc = minidom.parseString(source)
    status = xmldoc.getElementsByTagName('status')[0].firstChild.data
    if status == 'success':
        if getUserProfile() == '1':
            pass
            #getFavouriteShows()
        else:
            print('MyItasa non attivo')
    else:
        print('Errore nella ricerca dei prossimi episodi')
        error = xmldoc.getElementsByTagName('error')[0].firstChild.data
        print(error)


# Scarica sottotitoli italiani
def downloadSub(filePath):
    subPath = setup.getSetting('subtitles')
    if not os.path.isdir(subPath):
        os.makedirs(subPath)

    # Determino serie, ep, itasaShowId e itasaSubId  
    file = os.path.basename(filePath)
    match = re.search(r'.+\.S[0-9][0-9]E[0-9]+', file).group(0)
    name, ep = match.split('.S')

    name = name.replace('.', ' ')
    ep = str(int(ep[:2]))+'x'+ep[3:]
    if name == 'Castle 2009': name = 'Castle'
    if name == 'The Flash 2014': name = 'The Flash'
    itasaShowId = getShowsBySearch(name)
    itasaSubId = getSubtitle(ep, showId=itasaShowId)
    if not itasaSubId:
        return False

    # Recupero username e password
    with open('impostazioni.txt', 'r') as file:
        content = file.read()
        file.close()

    user = setup.getSetting('itasaUser')
    passwd = setup.getSetting('itasaPass')
    if not user or not passwd:
        user = input('Username Itasa: -> ')
        passwd = input('Password Itasa: -> ')

        newContent = content+'\nitasaUser='+user+'\nitasaPass='+passwd
        with open('impostazioni.txt', 'w') as file:
            content = file.write(newContent)
            file.close()

    # Login itasa
    url = 'http://www.italiansubs.net/index.php'
    headers = {'User-Agent': 'AssKickSeries 0.1'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('Initiate Failed')

    login_parameter = {'username': user,
                       'passwd': passwd,
                       'remember': 'yes',
                       'Submit': 'Login',
                       'remember': 'yes',
                       'option': 'com_user',
                       'task': 'login',
                       'silent': 'true'}

    session = requests.session()
    r = session.post(url, data=login_parameter, headers=headers)
    if not re.search('logouticon.png', r.text):
        print('Itasa login failed')
        return False
    else:
        pass

    # Scarico zip, estraggo e rinomino ita.srt
    url = 'http://www.italiansubs.net/index.php?option=com_remository&Itemid=6&func=fileinfo&id='
    response = session.get(url+itasaSubId, headers=headers)
    downloadLink = re.search(r'http://\S+'+itasaSubId+'\S+html=1', response.text)
    if downloadLink:
        response = session.get(downloadLink.group(0), headers=headers)
        if response:
            file = open(subPath+'ita.zip', 'wb')
            file.write(response.content)
            file.close()
            
            with zipfile.ZipFile(subPath+'ita.zip', 'r') as z:
                z.extractall(subPath)
            os.remove(subPath+'ita.zip')

            for file in os.listdir(subPath):
                if file.endswith('itasa.srt'):
                    os.rename(subPath+file, subPath+'ita.srt')
            
            print('Sottotitoli italiani scaricati correttamente')
            return True
        else:
            print('Sottotitoli italiani non trovati')
            return False
    else:
        print('Sottotitoli italiani non trovati')
        return False
