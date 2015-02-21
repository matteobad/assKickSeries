import re
import os
import shutil

# Restitisce settaggio richiesto
def getSetting(param, name=''):
    file = open('impostazioni.txt', 'r')
    content = file.read()
    file.close()

    try:
        match = re.search(param+'.+', content).group(0)
        setting = match.split('=')[1].replace('\n', '')
##        if param == 'location':
##            if name < 'The 100': return setting.split(';')[0]
##            else: return setting.split(';')[1]
##        else:
        return setting
    except:
        return False


# Crea impostazioni.txt al primo avvio
def defineSettings():
    pattern = r'[A-Z]+:.*$'
    mounted = re.findall(pattern, os.popen('mountvol /').read(), re.MULTILINE)
    moreSpace = 0
    for drive in mounted:
        try:
            total, used, free = shutil.disk_usage(drive)
            if free > moreSpace:
                location = drive+'serieTV\\'
                moreSpace = free
        except:
            pass
        
    try: os.mkdir(location)
    except: pass
    downloads = 'C:\\Users\\'+os.getlogin()+'\\Downloads\\'
    subtitles = 'serieTV\\sub\\'
    language = 'Italian'
    quality = '720p'

    if not os.path.exists('impostazioni.txt'):
        with open('impostazioni.txt', 'w') as file:
            file.write('location='+location+'\n')
            file.write('downloads='+downloads+'\n')
            file.write('subtitles='+subtitles+'\n')
            file.write('language='+language+'\n')
            file.write('quality='+quality+'\n')


def firstLunch():
    if not os.path.exists('impostazioni.txt'):
        print('Determino impostazioni programma...')
        print('Potrai modificarle da impostazioni.txt')
        defineSettings()

    if not os.path.exists('serieTV'):
        os.mkdir('serieTV')
        print('Creo cartella serieTV')

    if not os.path.exists(getSetting('subtitles')):
        os.mkdir(getSetting('subtitles'))
        print('Creo cartella sottotitoli')

    if not os.path.exists(getSetting('downloads')):
        os.mkdir(getSetting('subtitles'))
        print('Creo cartella download')

