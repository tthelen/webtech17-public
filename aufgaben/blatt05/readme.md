Uni Osnabrück, Web-Technologien 2017

Übungsblatt 5
=============

Abgabefrist: bis Dienstag, 5.12.2016, 24 Uhr


Aufgabe 1: Erweiterung des Icon-Editors (20 Punkte):
---------------------------------------------------

Erweitern Sie den Icon-Editor um folgende Funktionen:

- **Malen**: Statt nur mit einzelnen Clicks auf Einzelzellen soll auch gemalt werden
  können, indem Sie mit gedrückter Maustaste über die Tabelle fahren und dabei
  alle berührten Zellen färben. (5 Punkte)
- **Füllen**: Es soll ein "Fill mode" aktiviert werden können, der nicht nur eine einzelne Zelle färbt, 
  sondern die angeklickte Zelle und (rekursiv) alle benachbarten Zellen mit der gleichen Farbe. Bei aktiviertem
  Füllmodus soll ein anderer, das Füllen symbolisierende Mouse-Cursor verwendet werden. 
  (Tipp: `document.body.style.cursor = "url('/url/to/required/image.jpg')";`) (5 Punkte)
- **Pinselbreite**: Führen Sie die Eigenschaft "Pinselbreite" ein, die regelt, wie groß die
  gesetzten Punkte (derzeit immer 1x1 Zellen/Pixel) sind. Mit einem Schieberegler (Tipp: <input type="range">)
  soll es möglich sein, für die Pinselbreite einen Wert zwischen 1 und 10 einzustellen, der dann dergestalt
  berücksichtigt wird, dass ein Klick anschließend n x n Zellen/Pixel große Punkte erzeugt, wobei der Klickpunkt
  links oben im entstehenden Quadrat ist. (5 Punkte)
- **Icons laden**: Es soll rein clientseitig möglich sein, eines der unter "vorhandene Icons" angezeigten Icons
  per Klick in den Editor zu übernehmen, um es zu bearbeiten und unter gleichem oder neuem Namen zu speichern.
  (Sie müssen dazu ein Image-Objekt erstellen, das mit der Data-URL als Quelle versehen wird und nach dem Laden
  dieser Quelle auf den Canvas-Kontext angezeigt wird. Anschließend können Sie die Pixel per getImageData auslesen)
  (5 Punkte)

Hinweise:

- Benutzen Sie KEINE Javascript-Bibliotheken, auch kein jQuery
- Alle Erweiterungen kommen ohne Veränderung des Server-Codes aus. Sie können den Server-Code aber ändern,
  wenn dadurch Teilaufgabe 4 für Sie einfacher wird.


