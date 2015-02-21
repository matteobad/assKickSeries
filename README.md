# assKickSeries Beta

assKickSeries è un semplice script scritto in python per gestire le proprie serie TV preferite in automatico, dal download degli episodi e dei sottotitoli (grazie all'interazione con kickAss e myItasa) al muxing, sempre automatico, dei due con tanto di titolo, stagione ed episodio corretti. Il programma è stato creato causa pigrizia nel gestire le serieTV e nel tentativo di imparare un po' di python nel mentre.<br>
Ci tengo a precisare che è solo una versione beta, quindi potrebbe non funzionare a dovere. Ci sto ancora lavorando...<br>
Per funzionare il programma necessita di: <a href="http://www.python.it/download/">Python34</a>, comprese le librerie <a href="https://pypi.python.org/pypi/requests">requests</a> e <a href="https://pypi.python.org/pypi/lxml/3.4.2">lxml</a>, dei <a href="http://aranzulla.tecnologia.virgilio.it/come-impostare-dns-19767.html">DNS di google</a> per poter accedere a kickAss e reperire le informazioni, di un account su <a href="http://www.italiansubs.net/">Itasa</a> per poter reperire i sottotitoli in italiano, ed infine di <a href="http://www.fosshub.com/MKVToolNix.html">MkvToolnix</a> per il muxing delle puntate.

Posizionare i file .py dove si vuole, purchè siano nella stessa directory
Avviare assKickSeries.py e selezionare l'opzione desiderata:

    Benvenuto in assKickSeries v1.0
    1: Inserisci una serie TV
    2: Elimina una serie TV
    3: Scarica nuovi episodi
    4: Avvia muxing episodi/sub
    5: Esci


# Guida all'uso
1: Dato un nome cerca e aggiunge in automatico una serie TV alla lista dei preferiti. Verranno creati due file, uno <i>"prefetiti.txt"</i> contenente tutte le serie TV aggiunte nel seguente formato: <b>"nome_serie;url_serie"</b>, e l'altro <i>"serieTV/nome_serie.txt"</i> col seguente formato: <b>"nome_serie 00x00 titolo_puntata; data_uscita(v/x)*". Inoltre la serie verrà aggiunta, se possibile, all'elenco preferiti di myItasa

2: Elimina una serie TV da entrambi i file, elimina le puntate scarica se richiesto ed elimina anche la serie TV dai preferiti di myItasa se richiesto.

3: Scarica in automatico tutti i nuovi episodi disponibili attraverso magnet link, perciò bisogna avere un client torrent installato. Appena aggiunti gli episodi verranno considerati con già visti *(v) se la data di uscita sarà "più vecchia di quella dell'esecuzione del programma" o *(x) non visti in caso contrario.

4: Per ogni episodio presente nella directory dei download verranno scaricati i rispettivi sub se disponibili tramite l'acount Itasa. Successivamente i sub verranno uniti al file video tramite mkvtoolnix (basta che sia installato lo script farà il resto). Assicurarsi di modificare il file impostazioni.txt se le impostazioni di deafual non soddisfassero le personali esigenze.

5: Termina l'esecuzione
