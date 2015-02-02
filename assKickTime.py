import datetime

months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

# Adatta le date agli episodi e ne cambia il formato
def dateConvert(listDate, length):
    result = []
    for i in range(length - len(listDate)):
        result.append('00-00-0000')
    for date in listDate:
        date = date[-11:]
        day = date[4:6].replace(' ', '0')
        month = months.get(date[:3])
        year = date[7:]
        result.append(day+'-'+month+'-'+year)
    return result


# Compara una stringa-data con quella odierna
def compareDate(string):
    if string != '00-00-0000':
        now = datetime.datetime.now()
        episode = datetime.datetime.strptime(string, "%d-%m-%Y")
        if now < episode:
            return False
        else:
            return True
    else:
        return False


# Controlla se l'episodio è da scaricare
def notDownloaded(episode):
    check = episode[-2]
    if check == 'x':
        if compareDate(episode[-12:-2]):
            return True
        else:
            return False
    else:
        return False

