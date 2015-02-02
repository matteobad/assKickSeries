import string, re, os
import assKickLib, assKickTime, assKickUrl

# Aggiunge nuova serie tv
def addSeries():
    if (os.path.exists('serieTV') == False):
        os.mkdir('serieTV')

    name = input('\nInserisci titolo serie TV: -> ').lower()
    #quality = input('Inserisci formato desiderato: -> ').lower()
    
    page = assKickLib.findSeriePage(name)
    if page:
        assKickLib.updateSerieFile(name, page)
        file = open('listaSerie.txt','a')
        file.write(name.title()+';'+page+'\n')
        file.close()
        print('Serie aggiunta con successo')
    else:
        print('Serie non trovata')
    main()


# Elimina serie tv
def delSeries():
    canc = input('\nQuale serie vuoi rimuovere? -> ').title()
    if os.path.exists('serieTV\\'+canc+'.txt'):
        os.remove('serieTV\\'+canc+'.txt')
        print('File serie TV rimosso')
    else:
        print('File serie TV inesistente')
        
    file = open('listaSerie.txt', 'r+')
    content = file.read()
    if re.search(canc, content):
        content = content.replace(canc+'\n', '')
        file.write(content)
        print('Serie rimossa dalla lista')
    else:
        print('Serie non in lista')
    print('Fatto')   
    file.close()
    main()
    

# Stampa elenco serie tv
def showSeries():
    seriesList = open('listaSerie.txt').read().splitlines()
    print('\n')
    for serie in seriesList:
        print(serie.split(';')[0])
    main()
        

# Scarica nuove puntate
def downloadNew():
    print('Scarico lista torrent')
    assKickUrl.updateAPI()

    seriesList = open('listaSerie.txt').read().splitlines()
    print('Cerco download disponibili...')
    for serie in seriesList:
        name, page = serie.split(';')
        print('Cerco episodi per  '+name)
        assKickLib.updateSerieFile(name, page)
        serieFile = open('serieTV//'+name.lower()+'.txt', 'r+')
        row = serieFile.readline()
        while row:
            if assKickTime.notDownloaded(row):
                assKickLib.downloadEpisode(row)
                serieFile.seek(serieFile.tell()-3)
                serieFile.write('v')
                serieFile.seek(serieFile.tell()+3)
            row = serieFile.readline()
    print('Fatto')
    serieFile.close()
    main()
    
         
def main():
    print('''
    Benvenuto in assKickSeries v1.0\n
    1: Inserisci una serie
    2: Elimina una serie
    3: Visualizza lista serie
    4: Scarica nuove puntate
    5: Esci
    ''');
    choice= input('    -> ')
    
    if choice == '1': addSeries()
    elif choice == '2': delSeries()
    elif choice == '3': showSeries()
    elif choice == '4': downloadNew()
    elif choice == '5': exit()
    else: print('\tScelta non contemplata')

if __name__ == '__main__':
    main()
