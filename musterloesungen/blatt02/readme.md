Webtechnologien 2017/2018

Blatt 02
========


Hinweise zur Abgabe:
--------------------

Abgabefrist: Montag, 06.11.2017, 24 Uhr


Hinweise zur Bewertung:
-----------------------

* Geben Sie lauffähige Lösungen ab. Ist Ihre Lösung nicht lauffähig, fügen Sie einen Kommentar hinzu, der erläutert,
  wo Sie die Probleme vermuten und wie Sie den Fehler bereits gesucht haben.
* Für nicht lauffähige Programme, die keinen solchen Kommentar enthalten, können Sie maximal 50% der Punkte bekommen.
* Bezeichner müssen sprechend gewählt werden und alle Programme müssen sinnvoll kommentiert werden.
* Beachten Sie Details wie vorgegebene Dateinamen, Funktionsnamen etc. Abweichungen erschweren die Bewertung
  und führen zu Abzügen.
* Alle Text- und Quellcode-Dateien müssen UTF-8-codiert sein.


Aufgabe 1: Content-Encoding (14 Punkte)
---------------------------------------

Bandbreite ist ein knappes Gut und sollte wenn möglich schonend verwendet werden. 
So ist es üblich, die Inhalte von http-Responses komprimiert zu übertragen. Dabei
unterstützt http unterschiedliche Komprimierungsverfahren und überlässt es Client
und Server, sich über die Kompromierung zu verständigen.

Dabei gilt folgender Ablauf:
1. Der Client fügt ein Header-Feld `Accept-Encoding` dem Request-Header hinzu und listet als Wert des
   Feldes alle von ihm akzeptierten Komprimierungsverfahren kommagetrennt auf. Typisch ist ein Wert
   wie `Accept-Encoding: deflate, gzip`.
2. Der Server entscheidet anhand der Liste, der eigenen Fähigkeiten und ggf. des auszuliefernden Contents,
   ob und wie komprimiert wird. Der Response-Body wird dann komprimiert und der verwendete Algorithmus
   im Response-Header-Feld `Content-Encoding` festgehalten, z.B. `Content-Encoding: gzip`.
   
Modifizieren Sie die Datei `file_server.py` so, dass der Server einen eventuell vorhandenen 
`Accept-Encoding`-Header in Requests auswertet und seine Antwort mit dem `gzip`-Verfahren komprimiert,
falls die Codierung `gzip` vom Client akzeptiert wird. Falls nicht, wird der Response-Body nicht komprimiert,
der `Content-Encoding`-Header kann in diesem Fall entfallen oder den Wert `identity` erhalten.

Die `gzip`-Komprimierung können Sie in Python mit dem Modul zlib (s. https://docs.python.org/3/library/zlib.html)
vornehmen.

Aufgabe 2: Index (6 Punkte)
-----------------------------

Wird keine konkrete Datei angefordert soll eine Index-Liste ausgegeben werden, die alle Dateien im Ordner 
`static` auflistet. Die Auflistung kann als reiner Text oder HTML erfolgen. Setzen Sie in beiden Fällen einen 
korrekten Content-Type.

Hinweis:
* Die Funktion `listdir()` aus dem `os`-Modul liefert eine Liste von Dateien in einem Verzeichnis.



