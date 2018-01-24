Uni Osnabrück, Web-Technologien 2017

Übungsblatt 10
==============

Abgabefrist: bis Freitag, 02.02.2018, 24 Uhr

Aufgabe 1 (15 Punkte): Dateien neu anlegen, editieren und löschen
------------------------------------------------------------------

Ergänzen Sie die in der Vorlesung vorgestellte REST-Anwendung.

Start der Anwendung:
- python file_server_rest.py
- Startseite der Anwendung: http://localhost:8080/static/file_client_rest.html
- Startpunkt des REST-Interfaces: http://localhost:8080

Vervollständigen Sie die im Client-Interface bereits angelegten Funktionen
zum Anlegen, Bearbeiten und Löschen von Dateien. Die Anwendung soll weiterhin
als Single-Page-App funktionieren. Dazu müssen Sie vor allem REST-Requests im
Client ergänzen. Fehlende REST-Routen im Server sind ggf. ebenfalls zu 
ergänzen. Die Bearbeitung des Dateiinhaltes soll in einer Textarea geschehen.

Optionen:
- Sie können den Python-basierten Server verwenden (einfacher), oder einen node.js-Server entwickeln 
  (aufwendiger)
- Wenn Sie wollen, können Sie webpack verwenden, Sie können die Organisation des Client-Codes aber auch   
  beibehalten
  
Aufgabe 2 (5 Punkte): Authentifizierung
---------------------------------------

Versehen Sie das gesamte REST-Interface (alle Routen) mit einer 
http-Basic-Authentifizierung, die den Nutzer einmalig nach Zugangsdaten 
fragt. 

http Basic-Authentifizierung ist die einfachste Authentifizierungsart, die in REST-Interfaces häufig
verwendet wird. 

Ablauf:

1. Request enthält Authorization-Header mit Kennzeichnung des Authentifizierungsmechanismus und 
   Base64-codiertem String aus Benutzername, Doppelpunkt und 
   Passwort (in Javascript: `btoa(username+":"+password)`)
   
   Beispiel-Header (String: `admin:admin` ) :
   
   `Authorization: Basic YWRtaW46YWRtaW4=`

2. Der Server decodiert und prüft, ob Benutzername und Passwort korrekt sind. Falls ja, wird die
   gewünschte Aktion ausgeführt, falls nein (oder wenn Authorization-Header fehlt) wird folgende 
   Antwort geliefert:
   
   401 UNAUTHORIZED
   WWW-Authenticate: Basic realm="Bitte Passwort eingeben"
   
   Der Realm ist eine Art Erklärung oder Eingabeaufforderung,
   die natürlich nur in interaktiven Szenarien genutzt wird.
   Trifft der Browser auf so eine Antwort, blendet er ein eigenes
   Eingabeformular ein (s. https://httpbin.org/basic-auth/admin/admin 
   (Benuzername und Passwort sind `admin`)). Dieses Formular sollen
   Sie nicht verwenden, sondern ein eigenes (HTML-Formular).

Sie benötigen folgendes:
1. Auf Server-Seite eine Datenbank (Datei) mit Benutzernamen und Passwörtern.
2. Auf Client-Seite eine Abfrage von Benutzername und Passwort
3. Auf Client-Seite eine Codierung der Zugangsdaten und Übergabe den die AJAX-Requests, 
   z.B. per setRequestHeader)
4. Auf Server-Seite eine Überprüfung der Zugangsdaten 

Hinweise:
- Falls Sie Probleme damit haben, dass der Browser ein Eingabeformular
  einblendet, können Sie die Authentifizierungsmethode auch anders
  benennen, z.B. "RESTBasic" - es muss dann nur server- und clientseitig
  identisch genutzt werden.
  