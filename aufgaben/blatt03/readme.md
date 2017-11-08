Webtechnologien 2017/2018

Blatt 03
========


Hinweise zur Abgabe:
--------------------

Abgabefrist: Montag, 13.11.2017, 24 Uhr


Hinweise zur Bewertung:
-----------------------

* Geben Sie lauffähige Lösungen ab. Ist Ihre Lösung nicht lauffähig, fügen Sie einen Kommentar hinzu, der erläutert,
  wo Sie die Probleme vermuten und wie Sie den Fehler bereits gesucht haben.
* Für nicht lauffähige Programme, die keinen solchen Kommentar enthalten, können Sie maximal 50% der Punkte bekommen.
* Bezeichner müssen sprechend gewählt werden und alle Programme müssen sinnvoll kommentiert werden.
* Beachten Sie Details wie vorgegebene Dateinamen, Funktionsnamen etc. Abweichungen erschweren die Bewertung
  und führen zu Abzügen.
* Alle Text- und Quellcode-Dateien müssen UTF-8-codiert sein.


Aufgabe 1: Index-App (10 Punkte)
--------------------------------

1.1 Erweitern der Bassiklasse `App` (4 Punkte)

Erweitern Sie dazu zunächst die Basisklasse `App` um einen Namen der App (konfigurierbar über einen 
Konstruktor-Parameter, Default-Wert ist der Name der App-Klasse) und eine Einstiegsroute, d.h. einen URL-Pfad,
der zum Einstieg in die App genutzt werden kann.

1.2 Implementation einer Klasse `IndexApp` (4 Punkte)

Erstellen Sie eine App-Klasse `IndexApp`, die typischerweise mit leerem Präfix, d.h. für den Wurzelpfad registriert wird und eine Start-
bzw. Indexseite für den Server ausliefert. 

Diese Seite soll enthalten:
* Die Ausgabe eines Servernamens, der per Parameter beim Initialisieren der App gesetzt werden kann
* Die Ausgabe aller registrierten Apps mit ihrem Namen und der Einstiegsroute

1.3 Implementation einer Demo-Anwendung (2 Punkte)

Implementieren Sie eine Demo-Anwendung, die eine Instanz der Klasse `IndexApp` für den Wurzelpfad verwendet und 
mindestens drei weitere Apps bzw. App-Instanzen beinhaltet.


Aufgabe 2: E-Tag-Caching (10 Punkte)
------------------------------------

Bandbreite ist immer noch ein knappes Gut und noch besser, als den Inhalt komprimiert zu schicken (s. Blatt 1) ist es,
ihn gar nicht senden, wenn es nicht nötig ist. HTTP 1.1 definiert verschiedene Mechanismen, die es erlauben, bereits 
übertragene Inhalte zu cachen und bei späteren Aufrufen nicht erneut zu senden.

Einer dieser Mechanismen ist das so genannte `ETag`-Caching. Dabei wird bei der ersten Antwort ein eindeutiger Tag für 
die akutelle Version des Inhaltes (d.h. den Response-Body) mitgesandt. Bei späteren Anfragen enthält die Client-Anfrage 
diesen Tag und der Server kann prüfen, ob sich der Inhalt der angeforderten Ressource geändert hat. 
Falls nicht, signalisiert er lediglich, dass die beim Client noch vorhandene Version noch gültig ist 
und der Inhalt muss nicht erneut übertragen werden.

Auf HTTP-Ebene bildet sich dieses Verfahren wie folgt ab:

1. Bei jeder Antwort sendet generiert der Server ein für den Inhalt eindeutiges Tag und liefert es als Wert des 
   Response-Header-Feldes `ETag` mit (der Wert wird als "gequoteter String" angegeben, also mit doppelten 
   Anführungszeichen).
2. Wenn ein Client zu einer anzufordernden Ressource noch eine Kopie im Cache besitzt, sendet er deren `ETag` als 
   Wert des Request-Header-Feldes `If-None-Match`.
3. Der Server prüft nun, ob der aktuelle `ETag` der angeforderten Ressource mit dem im Request 
   übermittelten `ETags` übereinstimmt. Falls ja, antwortet er mit Status-Code `304 Not Modified` und 
   leerem Response-Body. (Hinweis: Im Standard sind auch mehrere Etags und "schwache Etags" vorgesehen, das muss
   hier nicht umgesetzt werden.)
   
Eine Möglichkeit zur Berechnung des `ETag` ist es, einen kryptographischen Hashwert aus dem fertig generierten 
Response-Body zu berechnen. In Python können dafür Klassen aus der `hashlib`-Bibliothek verwendet werden, 
z.B. der `sha256`-Algorithmus. Die Methode `.hexdigest()` erzeugt eine übermittelbare Hexadezimal-Repräsentation 
eines Hashwertes.

Erweitern Sie das Framework um eine automatische Unterstützung von `ETag`-Caching. 

Dokumentieren Sie die 
Funktionsfähigkeit der Implementation durch einen Developer-Tool-Screenshot aus Ihrem Browser (als `jpg`-Datei), 
der zeigt, dass bei einer  erneuten Anfrage der gleichen, unveränderten Ressourse der Server mit `304` antwortet 
und keinen Body sendet.
