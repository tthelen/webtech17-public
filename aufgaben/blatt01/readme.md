Webtechnologien 2017/2018

Blatt 01
========


Hinweise zur Abgabe:
--------------------

Abgabefrist: Montag, 30.10.2017, 24 Uhr


Hinweise zur Bewertung:
-----------------------

* Geben Sie lauffähige Lösungen ab. Ist Ihre Lösung nicht lauffähig, fügen Sie einen Kommentar hinzu, der erläutert,
  wo Sie die Probleme vermuten und wie Sie den Fehler bereits gesucht haben.
* Für nicht lauffähige Programme, die keinen solchen Kommentar enthalten, können Sie maximal 50% der Punkte bekommen.
* Bezeichner müssen sprechend gewählt werden und alle Programme müssen sinnvoll kommentiert werden.
* Beachten Sie Details wie vorgegebene Dateinamen, Funktionsnamen etc. Abweichungen erschweren die Bewertung
  und führen zu Abzügen.
* Alle Text- und Quellcode-Dateien müssen UTF-8-codiert sein.


Aufgabe 1 (8 Punkte)
--------------------

Erstellen Sie eine JSON-Datei `members.json`, die wie folgt strukturiert ist:

Auf oberster Ebene gibt es ein Dictionary (bzw. Objekt) mit zwei Schlüsseln (Keys):

1. `"name"`: Der Team-Name (String)

2. `"members"`: Eine Liste von mindestens 3 Mitgliedern.
       Jedes Mitglied wird durch ein Dictionary repräsentiert,
       das folgende Schlüssel enthält:
          
          "firstname" - Der Vorname (string)
          "lastname" - Der Nachname (string)
          "githubname" - Der Github-Benutzername (string)
          "studipname" - Der Stud.IP-Benutzername (string)
          
Hinweise:

* Eine kurze JSON-Einführung finden Sie unter: https://www.digitalocean.com/community/tutorials/an-introduction-to-json
* Einen JSON-Validator finden hier unter: https://jsonformatter.curiousconcept.com/
* Typische Fallen bei JSON:
    * JSON-Strings werden immer in doppelte Anführungszeichen eingeschlossen, nicht in einfache
    * Auch die Schlüssel in Dictionaries (bzw. Objekten) sind Strings, d.h. benötigen Anführungszeichen

Aufgabe 2 (10 Punkte)
---------------------

Schreiben Sie ein Python-Programm `members.py`, das diese json-Datei einliest und daraus eine HTML-Datei `members.html`
generiert, die eine Überschrift (`<h1>Text der Überschrift</h1>`) und eine Tabelle enthält. 
Die Tabelle soll sinnvolle Überschriften für die 4 Spalten haben und je Eintrag in der members-Liste 
eine Zeile mit Daten enthalten. Das Programm kann davon ausgehen, dass die eingelesenen Daten korrekt sein
(keine Fehlerbehandlung).
 
Eine HTML-Tabelle hat folgendes Muster (`<!-- ... -->` ist ein Kommentar, Zeilenumbrüche sind nicht relevant):

    <table>      <!-- Markiert den Beginn einer Tabelle -->
      <tr>       <!-- table row = Markiert Beginn einer Zeile -->
        <td>     <!-- table data = Markiert den Beginn einer Tabellenzelle -->
          Inhalt der 1. Zelle in der ersten Zeile
        </td>    <!-- markiert das Ende der Zelle -->
        <td>
          Inhalt der 2. Zelle in der ersten Zeile
        </td>
      </tr>      <!-- markiert das Ende der ersten Zeile -->
      <tr>
        <td>Inhalt von Zelle 1, Zeile 2</td>
        <ts>Inhalt von Zelle 2, Zeile 2</td>
      </tr>
    </table>
    
Prüfen Sie das Ergebnis, indem Sie die erzeugte Datei in einem Browser öffnen. Legen Sie einen Screenshot in 
einer Datei `members.jpg` bei.

Hinweise:
* Verwenden Sie unbedingt Python 3.x
* Verwenden Sie am besten die Datei `members.py` als Vorlage.
* Verwenden Sie keine grundsätzlich zusätzlich zu installierenden Bibliotheken, außer es wird im Aufgabenblatt anders 
angegeben
* Für das Parsen der json-Daten verwenden Sie das json-Modul aus der Python-Standardbibliothek (s. Vorlage)
* Auch andere Module der Standardbibliothek können Sie verwenden, sofern es Ihnen nötig erscheint (die Aufgabe kann aber gut 
ohne weitere imports gelöst werden)
* Für das Erzeugen der HTML-Datei können Sie einfache Python-String-Operationen verwenden
* Die eingelesene und die geschriebene Datei sollen bei im gleichen Verzeichnis wie das Python-Skript laufen
* Die Namen der einzulesenden und zu schreibenden Datei sollen im Programm festgelegt sein und müssen nicht über 
Kommandozeilenparameter bestimmt werden können


Aufgabe 3 (2 Punkte)
--------------------

Fügen Sie dem Programm aus Aufgabe 2 Fehlerbehandlungsfunktionen (per Exception-Handling) hinzu. Im Fehlerfall soll
das Programm auf der Standardausgabe die Meldung "Error!" ausgeben und einen Fehlergund angeben.

Abgefangen werden sollen mindestens folgende Fehler:
* Die einzulesende Datei ist nicht vorhanden oder kann nicht zum Lesen geöffnet werden
* Die Ausgabedatei kann nicht zum Schreiben geöffnet werden
* Die JSON-Datei kann nicht als JSON geparst werden
* Die JSON-Datei entspricht nicht dem erwartete Format

Hinweis:
* Exceptions müssen immer so spezifisch wie möglich gefangen werden
* Sie können Fehler auch über explizite Fehlerabfragen statt über Exceptions abfangen
