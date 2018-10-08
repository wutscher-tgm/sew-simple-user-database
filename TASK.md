# "Restful User-Service" - Taskdescription

## Einführung
Diese Übung gibt eine Einführung in die Verwendung von Restful-Services.

## Ziele
Das Verständnis von zustandslosen Verbindungen um Daten leicht administrieren und verteilen zu können.

## Voraussetzungen
* Grundverständnis von Python
* Lesen und Umsetzen von APIs
* Erstellung von Netzwerkverbindungen
* Automatisiertes Testen mittels Unit- und System-Tests

## Detailierte Ausgabenbeschreibung
Implementieren Sie eine einfache Userdatenbank, welche ein Erstellen, das Ausgeben, Updaten und Löschen über eine ReST-Schnittstelle ermöglicht. Verwenden Sie dazu eine einfache JSON-Struktur (z.B.: {id:1; username:"mmatouschek"; email:"mmatouschek@student.tgm.ac.at"; picture:"..."}). Die einzelnen User sollen nach dem Beenden des Server-Dienstes persistent gespeichert werden.  

Überprüfen Sie die CRUD-Funktionen mittels Unit- und System-Tests.  


## Bewertung
Gruppengrösse: 1 Person
### Anforderungen **überwiegend erfüllt**
+ CRUD Befehle mittels ReST-Schnittstelle auf lokaler Netzwerkschnittstelle
+ Benutzerphoto per Link
+ Ausführung und Dokumentation der Implementierung

### Anforderungen **zur Gänze erfüllt**
+ Benutzerphoto als Base64-Encoding
+ persistente JSON-Datenbasis 

## Quellen
[Flask ReST](https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example)
[Sqlite with Python](https://docs.python.org/3/library/sqlite3.html)

