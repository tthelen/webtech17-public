Uni Osnabrück, Web-Technologien 2017

Übungsblatt 8
=============

Abgabefrist: bis Dienstag, 16.01.2017, 24 Uhr

Aufgabe 1 (18 Punkte): TODO-Anwendung mit npm, Webpack, pure.css und jQuery
---------------------------------------------------------------------------

Entwickeln Sie eine rein clientseitige TODO-Listen-Anwendung mit folgenden Eigenschaften:
- Eine TODO-Liste besteht aus Einträgen, die über einen Text und einen Status (erledigt/nicht erledigt) 
  verfügen
- Über ein einzeiliges Eingabefeld können Einträge der TODO-Liste hinzugefügt werden, neue Einträge
  haben den Status "nicht erledigt"
- Die aktuelle TODO-Liste wird unter dem Eingabefeld dargestellt, jeder Eintrag hat eine Checkbox
  zum Ändern des Erledigt-Status und einen Löschen-Knopf oder -Link zum Entfernen des Eintrags
- Erledigte Einträge werden in hellerer Schrift und durchgestrichen dargestellt, nicht erledigte
  in dunklerer Schrift und ohne Text-Dekoration
- Beim Entfernen eines Eintrags wird der Eintrag sanft ausgeblendet (jQuery-Effekt)
- Beim ersten Aufruf wird die TODO-Liste mit 2-3 Default-Einträgen gefüllt

Die Einträge müssen nicht persistent gespeichert werden (s. Aufgabe 2), sondern werden bei jedem
Reload der Seite neu initialisiert. Sie können zum Speichern den DOM verwenden, d.h. dass außer
der Darstellung der Liste keine interne Repräsentation vorliegt.

Verwenden Sie für die Entwicklung folgende Tools und Bibliotheken:
- Alle Pakete - sowohl für die Entwicklung als auch für den Betrieb nötige Bibliotheken werden per npm 
  installiert. Sorgen Sie dafür, dass die Datei package.json alle notwendigen Informationen enthält,
  um die Bibliotheken mit einem einzigen Aufruf von `npm install` zu installieren.
- Nutzen Sie webpack, um eine gebundelte Datei zu erzeugen, die Javascript und CSS enthält. Konfigurieren
  Sie webpack über eine Konfigurationsdatei und verwenden Sie folgendes Verzeichnislayout:
  
    `/package.json` - npm-Konfigurationsdatei
    
    `/webpack.config.js` - webpack-Konfigurationsdatei
    
    `/src` - alle eigenen Javascript- und ggf. CSS-Quelldateien
    
    `/dist/index.html` - die (einzige) HTML-Seite
    
    `/dist` - Ausgabeverzeichnis für das Bundle
- Nutzen Sie den `webpack-dev-server` und ein `build`-Script, so dass per `npm run build` das Bundle 
  erstellt wird und ein Server startet, der die Anwendung unter `http://localhost:8080/dist` 
  verfügbar macht.
- Binden Sie pure.css über das npm-Paket `purecss` ein, konfigurieren Sie webpack so dass die 
  CSS-Datei(en) Teil des Bundles werden und nutzen Sie pure.css-Klassen in Ihrem HTML.
- Folgende Bibliotheken/npm-Pakete sind notwendig bzw. erlaubt:
  - webpack, webpack-dev-server, css-loader, style-loader
  - jquery, lodash (optional), purecss
  
**Wichtig**: Ihr Repository soll nur die notwendigen Dateien enthalten, d.h. weder von npm heruntergeladene
Pakete, noch die webpack-Ausgabe. (Eine ggf. zu erweiternde .gitignore-Datei liegt bei, Sie müssen diese aber 
nicht nutzen, sondern können auch manuell darauf achten, keine überflüssigen Dateien einzuchecken.)
    
Hinweise:
- Die Anwendung ist recht simpel zu erstellen, vor allem, wenn Sie jQuery konsequent nutzen. 
  Die Hauptschwierigkeit dieser Aufgabe liegt darin, die verschiedenen Tools "von null an"
  miteinander zu kombinieren und ans Laufen zu bekommen.


Aufgabe 2 (2 Punkte): Persistente Speicherung
--------------------------------------------

Erweitern Sie die TODO-Listen-Anwendung um eine (lokale, d.h. an den Browser gebundene) lokale 
Speicherung. Dazu gibt es verschiedene Technologien wie LocalStorage, WebSQL oder IndexedDB. 
Verwenden Sie die Bibliothek `localforage`, die eine sehr einfache API bietet und die beste für
den jeweiligen Browser verfügbare Basistechnologie auswählt.

Die persistente Speicherung soll folgendes leisten:
- Beim Laden der HTML-Seite soll die TODO-Liste auf dem lokalen Speicher rekonstruiert werden. Gibt
  es dort noch keine Einträge, sollen die in Aufgabe 1 erwähnten Default-Einträge verwendet und
  gespeichert werden.
- Speichern Sie jede Änderung (Eintrag anlegen, löschen, Status ändern) sofort im persistenten Speicher
- Sie können sich darauf verlassen, dass das Speichern klappt, d.h. Sie benötigen keine Fehlerbehandlung.
- Die Speicherung muss keine Effizienzüberlegungen berücksichtigen, d.h. Sie dürfen z.B. auch immer die 
  gesamte Liste unter einem einzigen Key speichern und lesen.
  
Im Erfolgsfall "überlebt" die Todo-Liste ein Neuladen der Seite, einen Neustart des Servers und auch 
einen Neustart des Browsers.
