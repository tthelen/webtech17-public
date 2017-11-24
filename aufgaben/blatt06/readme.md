Uni Osnabrück, Web-Technologien 2017

Übungsblatt 6
=============

Abgabefrist: bis Dienstag, 12.12.2016, 24 Uhr


Aufgabe 1: Authentifizierungs-Middleware (8 Punkte):
---------------------------------------------------

Implementieren Sie eine Middleware-Klasse, die für die Authentifizierung von Nutzern verwendet werden kann. Dabei gilt:
1. Der Benutername des aktuellen Benutzers wird in der Nutzer-Session unter dem Schlüssel "username" gespeichert.
2. Die Middleware erweitert das Request-Objekt um das Auth-Middlewareobjekt und stellt darüber eine Methode 
   `request.auth.check()` zur Verüfgung, die entweder den aktuellen Nutzernamen oder `false` liefert, falls der 
   aktuelle Nutzer nicht authentifiziert ist.
3. Die Nutzerdaten (Benutzername, Passwort) werden in einer JSON-Datei vorgehalten. (Später lernen wir effizientere 
   Methoden der Datenhaltung kennen.)
4. Die Middleware stellt außerdem eine Methode `request.auth.do()` bereit, die eine Login-Seite ausliefert, falls
   der aktuelle Nutzer nicht authentifiziert ist. Das dazu verwendete Template soll der Auth-Middleware bei der 
   Initialisierung übergeben werden können. Das Formular soll unter Beibehaltung alle Request-Parameter wieder an
   die gleiche URL gesendet werden. Die Middleware prüft dann in `do()`, ob ein Login-Versuch vorliegt und 
   verarbeitet ihn. Bei falschem Login wird das Login-Formular mit einer Fehlermeldung erneut eingeblendet.
5. Es soll auch ein Logout möglich sein.

Hinweise:
- Evtl. können `check()` und `do()` noch Parameter bekommen


Aufgabe 2: Umstellung des Wikis auf Templates und Authentifizierung (12 Punkte)
-------------------------------------------------------------------------------

1. Das Wiki soll Templates für die HTML-Erzeugung nutzen. Gehen Sie dabei von der Wiki-Implementation in diesem Repository 
aus. Es bleibt Ihnen überlassen, ob Sie Jinja2- oder Mustache-Templates verwenden. Setzen Sie sowohl gleichbleibende 
Bestandteile aller Seiten als auch die Seitenliste über den Template-Mechanismus um. (6 Punkte)

2. Im Wiki sollen das Editieren von Seiten und die Verwendung des "Neue Seite anlegen"-Formulars nur für authentifizierte 
Nutzer möglich sein. (6 Punkte) Dabei gilt folgendes:
    - Legen Sie mindestens zwei Nutzer an, einer davon muss den Benutzernamen "wiki" und das Passwort "wiki" haben.
    - Legen Sie ein Login-Template an, das mit der Authentifizierungsmiddleware funktioniert und auch eine 
      Abbruchmöglichkeit biete. 
    - Bieten Sie ein "Lazy Login" an, d.h. erst bei Aufruf einer Aktion, die Authentifizierung benötigt, wird das 
      Login-Formular eingeblendet.
    - Bieten Sie zusätzlich ein explizites Login über einen Login-Knopf auf jeder Seite an.
    - Bieten Sie für eingeloggte Nutzer ein Logout über einen Logout-Knopf auf jeder Seite an.
     
Hinweise:

- Prüfen Sie bei der Verwendung des Template-Mechanismus genau, welche Ausgaben escaped werden müssen, 
  und welche nicht. 
- Prüfen Sie sorgfältig, welche Aktionen eine Authentifizierung benötigen 
  (Tipp: Eine Aktion wird dabei häufig übersehen).
  
  