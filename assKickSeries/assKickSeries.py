import re
import os
import estract
import update
import download


# Aggiunge una nuova serie TV
def addSerie():
    if not os.path.exists('serieTV'):
        os.mkdir('serieTV')

    name = input('\nNome serie TV: -> ').lower()
##    with open('database.txt','r') as db:
##        content = db.read()
##        match = re.findall('.+'+name.title()[1:]+'.+', content)
##        db.close()
##        
##    if len(match) > 1:
##        print(len(match),' possibili riscontri\n')
##        for i in range(len(match)):
##            print(i+1, match[i])
##        index = int(input('\nQuale (numero corrispondente): -> '))
##        name, page = match[index-1].split(';')
##        print('Ok cerco', name, '...')
##    elif len(match) == 1:
##        print('Serie trovata, aggiungo...')
##        name, page = match.split(';')
##    else:
    print('Nessun riscontro nel db, cerco online...')
    page = estract.estractPage(name)

    if page:
        if not os.path.exists('preferiti.txt'):
            file = open('preferiti.txt', 'w')
            file.write(name.title()+';'+page+'\n')
            file.close()
        else:
            file = open('preferiti.txt', 'r+')
            content = file.read()
            if not re.search(name.title(), content):
                file.write(name.title()+';'+page+'\n')
            file.close()
        updateSerieFile(name, page)
        print('Serie aggiunta con successo')
    else:
        print('Serie non trovata')
    main()


# Aggiorna file serie TV
def updateSerieFile(name, page):
    newFile = ''
    source = estract.estractSource(page)
    episodes = estract.estractEpisodes(source)
    path = ''.join('serieTV\\'+name.lower()+'.txt')

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
            if download.compareDate(element):
                newFile += ''.join(name.title()+' '+element+'v\n')
            else:
                newFile += ''.join(name.title()+' '+element+'x\n')

    file = open(path, 'w')
    file.write(newFile)
    file.close()
    

# Elimina serie TV
def delSerie():
    canc = input('\nQuale serie vuoi rimuovere? -> ').title()
    path = ''.join('serieTV\\'+canc+'.txt')
    if os.path.exists(path):
        os.remove(path)
        print('File serie TV rimosso')

    file = open('preferiti.txt', 'r+')
    content = file.read()
    if re.search(canc, content):
        content = content.replace(canc+'\n', '')
        file.write(content)
        print('Serie rimossa dalla lista')
    file.close()
    main()


# Mostra elenco preferiti
def showFavourite():
    file = open('preferiti.txt','r')
    content = file.read().splitlines()
    for serie in content:
        print(serie.split(';')[0])
    file.close()
    main()
        

# Scarica nuove puntate
def downloadNew():
    print('\nScarico lista torrent...')
    update.updateAPI()

    preferiti = open('preferiti.txt', 'r')
    content = preferiti.read().splitlines()
    for element in content:
        name, page = element.split(';')
        print('Cerco episodi per', name)
        updateSerieFile(name, page)
        download.newEpisodes(name)
    preferiti.close()
    main()


# Menù principale
def main():
    print('''
Benvenuto in assKickSeries v1.0\n
1: Inserisci una serie
2: Elimina una serie
3: Visualizza lista serie
4: Scarica nuove puntate
5: Esci
''');
    choice= input('-> ')
    
    if choice == '1': addSerie()
    elif choice == '2': delSerie()
    elif choice == '3': showFavourite()
    elif choice == '4': downloadNew()
    elif choice == '5': exit()
    else: print('\tScelta non contemplata')


if __name__ == '__main__':
    main()

    
