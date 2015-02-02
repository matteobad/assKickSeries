# assKickSeries Beta

assKickSeries è un semplice programma scritto in python per gestire le proprie serie TV preferite in automatico, dal download degli episodi e dei sottotitoli (grazie all'interazione con kickAss e myItasa) al muxing, sempre automatico, dei due con tanto di titolo, stagione ed episodio corretti. Il programma è stato creato causa pigrizia nel gestire le serieTV e nel tentativo di imparare un po' di python nel mentre.<br>
Ci tengo a precisare che è solo una versione beta, anzi alpha, quindi potrebbe non funzionare a dovere. Ci sto ancora lavorando...<br>
Per funzionare il programma necessita dei DNS di google per poter accedere a kickAss e reperire le informazioni, se non sapete come impostarli potete seguire questa guida: http://aranzulla.tecnologia.virgilio.it/come-impostare-dns-19767.html

Posizionare i file .py dove si vuole, purchè siano nella stessa directory
Avviare assKick.py e selezionare l'opzione desiderata:

    Benvenuto in assKickSeries v1.0
    1: Inserisci una serie
    2: Elimina una serie
    3: Visualizza lista serie
    4: Scarica nuove puntate
    5: Esci


# Guida all'uso
1: Dato un nome cerca e aggiunge in automatico una serie TV alla lista dei preferiti. Verranno create due file, uno "listaSerie.txt" contenente tutte le serie TV aggiunte nel seguente formato: <b>"nome_serie;url_serie"</b>, e l'altro "serieTV/nome_serie.txt" col seguente formato: <b>"nome_serie 00x00 titolo_puntata; data_uscita(v/x)*".

2: Elimina una serie TV da entrambi i file.

3: Stampa a video l'elenco delle serie TV nei preferiti, ovvere nel file "serieLista.txt".

4: Scarica in automatico tutti i nuovi episodi disponibili attraverso magnet link, perciò bisogna avere un client torrent installato. Appena aggiunti gli episodi verranno considerati con già visti *(v) se la data di uscita sarà "più vecchia di quella dell'esecuzione del programma" o *(x) non visti in caso contrario.

5: Termina l'esecuzione
