Uni Osnabrück, Web-Technologien 2017

Übungsblatt 9
=============

Abgabefrist: bis Dienstag, 23.01.2017, 24 Uhr

Aufgabe 1 (2 Punkte): Fehlerbehandlung im expresswiki
-----------------------------------------------------

Füllen Sie die Fehlerbehandlungs-Middleware so, dass das wikierror.mustache-Template verwendet wird und die Platzhalter 
korrekt gesetzt werden. Führen Sie eine Fehlerbehandlung für die Fälle ein, dass der Route save der Seitenname fehlt 
oder kein Text übergeben wird.


Aufgabe 2 (2 Punkte): Create-Page-Funktion im expresswiki
---------------------------------------------------------

Ergänzen Sie die im Template bereits angelegte Funktion, eine neue Seite anzulegen. 
In das Formular soll der Name der neuen Seite eingegeben werden. Der Server überprüft dann, ob der eingegebene 
Seitenname gültig ist. Falls nein, wird eine Fehlermeldung über den Mechanismus aus Aufgabe 1 ausgegeben, 
falls ja, wird die neue Seite mit Defaulttext zum Editieren geöffnet.


Aufgabe 3 (10 Punkte):  Edit verhindern, wenn noch jemand editiert
------------------------------------------------------------------

Implementieren Sie eine Funktion, die den Aufruf der Editieransicht einer Seite verhindert, wenn ein anderer
Nutzer die gleiche Seite gerade editiert. 

Gehen Sie dazu wie folgt vor:

1. Definieren Sie einen webpack-basierten Build-Prozess, der alle benötigten Javascript-Daten in einer 
Datei bundle.js zusammenfasst. Dies umfass sowohl selbst geschriebene Teile als auch Bibliotheken.
1. Erstellen Sie eine clientseitig auszuführende Datei wiki.js, die in alle Templates eingebunden wird und 
die Startpunkt für webpack ist.
2. Schreiben Sie sauberen Javascript-Code: Keine Eventhandler im HTML-Code definieren, kein Javascript-Code
direkt in den Templates und sinnvolle Strukturierung inkl. Kommentaren.
3. Verwenden Sie socket.io, um bei Aufruf der Editier-Ansicht eine socket.IO-Verbindung zum Server zu öffnen. 
4. Der Server führt eine Liste der gerade zum Editieren geöffneten Dateien (reagiert auf connection und 
disconnect-Events von socket.io) und liefert statt der Editieransicht bei Aufruf von /edit eine sinnvolle
Fehlermeldung, solange noch ein Client die Editieransicht der angeforderten Seite geöffnet hat.


Aufgabe 4 (6 Punkte): Live-Änderungsansicht
-------------------------------------------

Verändern Sie die /show-Ansicht so, dass Änderungen an der Seite durch einen andern Nutzer / in einem anderen 
Tab oder Fenster sofort sichtbar werden, d.h. während des Tippens und bereits vor dem Absenden.

Reagieren Sie dazu clientseitig auf das input-Event der textarea und senden Sie jeweil den vollständigen 
aktuellen Text per socket.io-Nachricht an den Server, der sie an alle Clients verteilt, die gerade die Show-Ansicht
der betreffenden Seite geöffnet haben.


Hinweise:
- Der Buildprozess soll per `npm run build` gestartet werden können
- Der Server soll per `npm start` gestartet werden können
- Die Lösung soll in einem aktuellen Firefox funktionieren
