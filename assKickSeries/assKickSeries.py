#########################################################################
#                                                                       #
#  Leggere README.txt contenete guida all'uso                           #
#                                                                       #
#  Benvenuto in AssKickSerie un piccolo script scritto in python        #
#  utile per la gestione delle prorpie serie TV preferite, grazie       #
#  all'integrazione con itasa e kickAssTorrent dai quali vengono        #
#  recuperati i nuovi episodi e sottotitoli.                            #
#  Il prgramma gestisce una lista di serie TV/anime preferiti           #
#  (con pieno supporto a myItasa), creando e mantenendo organizzata     #
#  una libreria contenente tutte le puntate scaricate giorno per        #
#  giorno, complete di sub ita (muxati tramite mkvtoolnix) e titolo     #
#  episodio corretto.                                                   #
#                                                                       #
#  Modificare il file impostazioni.txt a proprio piacimento e avviare   #
#  AssKickSeries dal quale potrete:                                     #
#  - Aggiungere serie TV (sincrozzato con myItasa)                      #
#  - Eliminare una serie TV dai preferiti                               #
#  - Scaricare le nuove puntate nel formato desiderato (automatico)     #
#  - Avviare muxing nuovi episodi coi sub nella lingua impostata        #
#                                                                       #
#########################################################################

import kat
import itasa
import mkvtoolnix
import setup
import os
import re
import html
import requests
import subprocess



SPECIAL = ['/', '*', '?', '"', '<', '>', '|']



# Aggiungo nuova serie TV
def addSerie(name='', itasaShowId=''):
    if name == '':
        name = input('\nNome serie TV: -> ').lower().title()
    if itasaShowId == '':
        itasaShowId = itasa.getShowsBySearch(name)
        
    print('Cerco', name, 'online...')
    page = kat.getShowPage(name)
    if page:
        updateSerie(name, page)
        itasa.addToMyItasa(itasaShowId)
        print(name, 'aggiunto con successo')
    else:
        print('Serie non trovata')



# Aggiorna file serie TV
def updateSerie(name, page):
    source = kat.getSource(page)
    episodes = kat.getEpisodes(source)
    season = kat.getSeasons(source)
    if name == 'Castle': name = 'Castle 2009'
    if name == 'The Flash': name = 'The Flash 2014'

    # Crea cartelle e sottocartelle ogni stagione della serie
    newFilePath = setup.getSetting('location', name)

    for ch in SPECIAL:
        name = name.replace(ch, '')
        
    path = os.path.join(newFilePath+name+'\\')
    if not os.path.isdir(path):
        os.makedirs(path)
    for i in range(season):
        pathSeason = ''.join(path+str(i+1)+'° Stagione')
        if not os.path.isdir(pathSeason):
            os.mkdir(pathSeason)

    # Aggiorna o crea file serie TV
    newFile = ''
    path = 'serieTV\\'+name+'.txt'
    try:
        file = open(path, 'r')
        for i in range(len(episodes)):
            line = file.readline()
            if line != episodes[i] and line[-2] == 'x':
                newFile += ''.join(name.title()+' '+episodes[i]+'x\n')
            else:
                newFile += line
        file.close()
    except:
        for element in episodes:
            if kat.compareDate(element):
                newFile += ''.join(name.title()+' '+element+'v\n')
            else:
                newFile += ''.join(name.title()+' '+element+'x\n')

    file = open(path, 'w')
    file.write(html.unescape(newFile))
    file.close()

    # Aggiorno preferiti.txt
    if not os.path.exists('preferiti.txt'):
        file = open('preferiti.txt', 'w')
        file.write(name+';'+page+'\n')
        file.close()
    else:
        file = open('preferiti.txt', 'r+')
        content = file.read()
        if not re.search(name, content):
            file.write(name+';'+page+'\n')
        file.close()


# Elimino serie TV
def delSerie():
    showFavourite()
    canc = input('\nNome seire TV da eliminare: -> ').title()

    # Rimuovo serie file
    path = ''.join('serieTV\\'+canc+'.txt')
    if os.path.exists(path):
        os.remove(path)
        print('Rimossa lista episodi per ', canc)
    else:
        print('Lista episodi inesistente per ', canc)
        
    # Rimuovo serie da preferiti
    if os.path.exists('preferiti.txt'):
        file = open('preferiti.txt', 'r')
        content = file.read()
        file.close()

        match = re.search(canc+'.+\n', content)
        try:
            with open('preferiti.txt', 'w') as file:
                content = content.replace(match.group(0), '')
                file.write(content)
                file.close()
            print(canc, 'rimosso dai preferiti')
        except:
            print(canc, 'non presente in preferiti')

    # Rimuovo episodi se richiesto
    answer = input('Vuoi cancellare anche gli episodi? (s/n)-> ').lower()
    if answer == 's':
        newFilePath = setup.getSetting('location')
            
        try:
            subprocess.call('RMDIR /S /Q '+newFilePath+canc)
            print('Episodi', canc, 'rimossi con successo')
        except:
            print('Non avevi episodi per', canc)
        
    else:
        print('Episodi non rimossi')

    # Rimuovo da myItasa se richiesto
    answer = input('Vuoi cancellare da myItasa? (s/n)-> ').lower()
    if answer == 's':
        itasaShowId = itasa.getShowBySearch(canc)
        itasa.removeFromMyItasa(itasaShowId)
    else:
        print('Serie TV non rimossa da myItasa')
        

# Mostra elenco preferiti
def showFavourite():
    if os.path.exists('preferiti.txt'):
        file = open('preferiti.txt', 'r')
        content = file.read().splitlines()
        file.close()
        print('\nLista preferiti:')
        for serie in content:
            print(serie.split(';')[0])
    else:
        print('\nDevi prima aggiungere dei preferiti')


# Scarica nuovi episodi e nuovi sottotioli
def downloadNew():
    print('\nScarico lista torrent...')
    kat.getHourlydump()

    if os.path.exists('preferiti.txt'):
        file = open('preferiti.txt', 'r')
        content = file.read().splitlines()
        file.close()
        for serie in content:
            # Scarico tutti i nuovi episodi
            name, page = serie.split(';')
            print('Cerco episodi per', name)
            updateSerie(name, page)
            try:
                kat.downloadNewEpisodes(name)
            except:
                print('Errore imprevisto nel download')
    else:
        print('Devi prima aggiungere dei preferiti')


# Effettua muxing
def startMuxing():
    mkvtoolnix.removeFolders()
    mkv = mkvtoolnix.getEpisodesList()

    if not mkv:
        print('\nPrima devi scaricare degli episodi')

    for episode in mkv:
        file = os.path.basename(episode)
        match = re.search(r'.+\.S[0-9][0-9]E[0-9]+', file).group(0)
        name, ep = match.split('.S')

        subprocess.call('RMDIR /S /Q '+setup.getSetting('subtitles'), shell=True)
        print('\nScarico sottotitoli per', name.replace('.', ' '), ep)
        if itasa.downloadSub(episode):
            itaSub = setup.getSetting('subtitles')+'ita.srt'   
            newFile = mkvtoolnix.getNewFilePath(name, ep)
            mkvmerge = mkvtoolnix.getMkvmergePath()+' -o '
            for ch in SPECIAL:
                newFile = newFile.replace(ch, '')
                
            cmd = mkvmerge+'"'+newFile+'" "'+episode+'" "'+itaSub+'"'
            if subprocess.call(cmd, shell=True) == 0:
                print('Muxing completato per', os.path.basename(newFile))
            else:
                print('Muxing fallito per', os.path.basename(newFile))

            try: os.remove(itaSub)
            except: pass

        else:
            print('Sottotitoli non ancora disponibili')


# Menù principale
def main():
    setup.firstLunch()
    if not os.path.exists('serieTV'):
        os.mkdir('serieTV')
        
    if not os.path.exists('preferiti.txt'):
        print('Non hai ancora aggiunto preferiti')
        answer = input('Posso aggiungerne da myItasa: (s/n) -> ').lower()
        if answer == 's':
            favourite = itasa.getFavouriteShows()
            for element in favourite:
                showId = element.split(';')[0]
                showName = element.split(';')[1]
                addSerie(showName, showId)
    
    print(''' __________________________________
|                                  |
| Benvenuto in assKickSeries v2.0  |
|                                  |
| 1: Inserisci una serie TV        |
| 2: Elimina una serie TV          |
| 3: Scarica nuovi episodi         |
| 4: Avvia muxing episodi/sub      |
| 5: Esci                          |
|__________________________________|
                                     ''')
    
    choice= input('-> ')
    
    if choice == '1': addSerie(); main()
    elif choice == '2': delSerie(); main()
    elif choice == '3': downloadNew(); main()
    elif choice == '4': startMuxing(); main()
    elif choice == '5': exit()
    else:
        print('\tScelta non contemplata')
        main()


if __name__ == '__main__':
    main()
    
