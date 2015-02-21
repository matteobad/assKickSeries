#######################################################
#                                                     #
#  Modulo per estrarre dati dal computer per trovare  #
#  mkvmerge, lista episodi scaricati da muxare, e     #
#  determinare percorso di destinazione per i file    #
#  in seguito al muxing                               #
#                                                     #      
#######################################################

import setup
import re
import os
import fnmatch
import shutil



# Determina lista HDD
def getDrivesLetter():
    pattern = r'[A-Z]+:.*$'
    mounted = re.findall(pattern, os.popen('mountvol /').read(), re.MULTILINE)
    return mounted


def getMkvmergePath():
    pattern = '*mkvmerge.exe'
    for root, dirs, files in os.walk('\\'):
        for filename in fnmatch.filter(files, pattern):
            mkvmerge = os.path.join(root, filename)
            if mkvmerge:
                return '"'+mkvmerge+'"'


# Restituisce lista file .mkv
def getEpisodesList():
    result = []
    downloadsDir = setup.getSetting('downloads')
    for root, dirs, files in os.walk(downloadsDir):
        for filename in fnmatch.filter(files, '*E[0-9][0-9]*.m??'):
            episode = os.path.join(root, filename)
            result.append(episode)
            
    return result


# Rimuove file e cartelle inutili
def removeFolders():
    downloadsDir = setup.getSetting('downloads')
    # Estrare episodi da cartelle e filtra sample
    for root, dirs, files in os.walk(downloadsDir):
        for filename in fnmatch.filter(files, '*[0-9][0-9]E[0-9][0-9]*.m??'):
            episode = os.path.join(root, filename)
            match = re.search(r'sample', episode)
            if not match:
                try: shutil.move(episode, downloadsDir)
                except: pass

        # Elimina cartelle
        for folder in dirs:
            if re.search(r'S[0-9]+E[0-9]+', folder):
                try: os.system('RMDIR /S /Q '+root+folder)
                except: pass


# Trova la cartella di destinazione del nuovo file
def getNewFilePath(name, episode):##
    file = open('serieTV/'+name.replace('.', ' ')+'.txt')
    content = file.read()
    file.close()
    
    # Trovo nome episodio da serie.txt
    match = re.search(r'.+'+episode[:2]+'x'+episode[3:]+'.+;', content).group(0)
    fileName = match.replace(';', '.mkv').replace(episode[:2], str(int(episode[:2])))
    muxedPath = setup.getSetting('location')

    if name == 'Castle.2009': name = 'Castle'
    if name == 'The.Flash.2014': name = 'The.Flash'
    path = muxedPath+name.replace('.', ' ')+'\\'+str(int(episode[:2]))+'° Stagione\\'+fileName
    return path
