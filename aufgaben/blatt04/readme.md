Webtechnologien 2017/2018

Blatt 04
========


Hinweise zur Abgabe:
--------------------

Abgabefrist: Montag, 20.11.2017, 24 Uhr


Hinweise zur Bewertung:
-----------------------

* Geben Sie lauffähige Lösungen ab. Ist Ihre Lösung nicht lauffähig, fügen Sie einen Kommentar hinzu, der erläutert,
  wo Sie die Probleme vermuten und wie Sie den Fehler bereits gesucht haben.
* Für nicht lauffähige Programme, die keinen solchen Kommentar enthalten, können Sie maximal 50% der Punkte bekommen.
* Bezeichner müssen sprechend gewählt werden und alle Programme müssen sinnvoll kommentiert werden.
* Beachten Sie Details wie vorgegebene Dateinamen, Funktionsnamen etc. Abweichungen erschweren die Bewertung
  und führen zu Abzügen.
* Alle Text- und Quellcode-Dateien müssen UTF-8-codiert sein.


Aufgabe 1: Wiki mit CSS-Framework stylen (10 Punkte)
----------------------------------------------------

In der Praxis werden Sie selten von Grund auf CSS-Klassen entwerfen, sondern in aller
Regel ein CSS-Framework verwenden. Für die folgenden Aufgaben sollen Sie jeweils das 
Framework pure.css (https://purecss.io/) benutzen. 

Die Einzelpunkte sind:
* Umstellung auf ein responsives Grid-System (4 Punkte)
* Füllen des Kopf- und Fußbereiches (2 Punkte)
* Füllen der Seitenleiste (2 Punkte)
* Füllen der Hauptanzeige mit dem Wikitext (2 Punkte)

Das Wiki soll ein Layout bekommen, wie es in der beiliegenden Datei layout.png skizziert. 
Verwenden Sie die pure-css-Layout-Klassen. Bei einer Anzeigebreite von weniger als 768 Pixel 
soll die Seitenleiste über dem Wiki-Text angezeigt werden, statt links daneben.

Verwenden Sie für Formulare, Buttons etc. die vorgesehenen Pure.css-Klassen. Wie Sie
das Framework einbinden, ist Ihnen überlassen. Falls Sie vorgefertigte Layouts o.ä.
verwenden, beachten Sie unbedingt die Lizenzen und Lizenzauflagen (z.B. Anfügen von
Autorenhinweisen, Lizenztexten etc.).

Verwenden Sie den vorgegebenen Template-Mechanismus aus der Klasse Response, ggf. mit
den Erweiterungen aus Aufgabe 4. Wenn Sie Aufgabe 4 nicht bearbeiten, sind 
HTML-Code-Dopplungen und HTML-Listen etc., die im Python-Code generiert werden, zulässig.


Aufgabe 2: Liste von Wiki-Seiten (4 Punkte)
-------------------------------------------

Integrieren Sie in die Seitenleiste eine aktuelle Liste der vorhandenen Wikiseiten 
als pure.css-Menu, das auf die Anzeige-Aktion der jeweiligen Seite verlinkt. 


Aufgabe 3: Formular zum Anlegen einer neuen Seite (4 Punkte)
------------------------------------------------------------

Integrieren Sie in die Seitenleiste ein Formular zum Anlegen einer neuen Wikiseite.
In das Formular soll der Name der neuen Seite eingegeben werden. Der Server überprüft
dann, ob der eingegebene Seitenname gültig ist. Falls nein, wird eine Fehlermeldung 
ausgegeben, falls ja, wird die neue Seite mit Defaulttext zum Editieren geöffnet.


Aufgabe 4: Erweiterung des Template-Mechanismus (2 Punkte)
----------------------------------------------------------

_Achtung: Die ist eine komplexere Aufgabe, die vor allem für diejenigen gedacht ist, 
die die Grundlagen schon gut beherrschen und nach Herausforderungen suchen._

Der vorgegebene Template-Mechanismus ist sehr simpel und kaum praxistauglich. Rüsten
Sie zwei wichtige Mechanismen von Template-Engines nach:

1. Verarbeitung von Sub-Templates (Partials). Der größte Teil der Ansichten für die 
Aktionen edit und show ist gleich, Sie sollten daher den HTML-Code für Beginn und Ende
der Seiten in zwei Teil-Templates auslagern, die in jeder Ansicht eingefügt werden.

2. Behandlung von Listen. Die Liste der Wikiseiten hat eine variierende Länge und
kann daher nicht ohne weiteres im Template abgebildet werden. Es soll daher eine
Möglichkeit geben, Teiltemplates wie hier eine einzelne Zeile im Seitenlisten-Menu 
wiederholt auszugeben.

Beide Aufgabeteile sollten durch eine Erweiterung der Template-Syntax gelöst werden,
die Sie selbst verarbeiten, bevor Sie den Python-Format-Mechanismus anwenden. Es ist
auch möglich, beide Mechanismen zusammen (mit kleinen Fallunterscheidungen) zu behandeln.

Für diese Aufgabe gibt es verschieden viele und verschieden aufwendige Lösungswege.
Es ist erwünscht, dass Sie sich auch zwischen den Gruppen über Lösungsansätze austauschen.
