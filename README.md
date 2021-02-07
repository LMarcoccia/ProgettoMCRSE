# ProgettoMCRSE

Repository della tesina per l'esame di Modellistica  e Controllo di Reti e Sistemi a Eventi

Link Utili:

https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat

https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat

https://openflights.org/data.html#airport


Il programma è composto da 3 file (temporanei):

-TesinaMCRSE: vengono importati i dataset delle infrastrutture e delle rotte. Successivamente vengono selezionati gli hub di tipo 'aeroporto' e che si trovano nel continente
 desiderato. Infine vengono specificati arrivi e partenze nel dataframe delle rotte. 

-Matrice: viene creata la matrice di adiacenza per gli aeroporti di un certo continente. Se due strutture sono collegate, il peso corrispondente nella matrice è la distanza geodesica
 tra di esse. Successivamente viene plottata su una mappa del continente esaminato la posizione esatta delle infrastrutture (se hanno grado maggiore o uguale a un parametro k) e 
 i collegamenti tra di esse.
 
-eigen: viene importata la matrice di adiacenza creata in precedenza e calcolata la matrice laplaciana. Ne vengono estratti gli autovettori e viene poi plottata la configurazione dei
 punti su uno scatterplot. 
 
 
Il programma è ancora in fase di sviluppo: seguiranno altre correzioni,sviluppi e riorganizzazioni dei file nella repository.