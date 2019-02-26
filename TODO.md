# 1. Semester

* [X] 12:55 TODO.md erstellen
* [X] 13:00 Git forken & upstream pushen
* [x] 13:10 Vue.js initialisieren -> ./src/main/vue/client
* [x] 13:15 Client mit Vue.js auf REST-Server verbinden (Auslesen der User)
* [x] 13:30 Cypress.io Test für das Listening der User schreiben
* [x] 13:40 Travis.yml erstellen und das neue origin/master (Fork) mit TravisCI einbinden und server/client Tests durchführen
* [x] 13:15 README erweitern und auf upstream/master pushen
* [x] 14:10 weitere GUI-Elemente implementieren/testen/dokumentieren

# 2. Semester

## CRUD authentifizieren

GK:
* [x] mit HTTP-Digest
* [ ] Vue Client Non Static DB
* [x] bestehende UserDB (min SHA256)

EK:
* [ ] OAUTH (switching: if no PW-Hash in UserDB)
* [x] Nur admin darf Create, Update, Delete
* [x] Lesen w/o PW-Hash für alle angemeldeten User

## Deployment

GK:
* [x] Lokal


EK:
* [x] global, z.B.: ~~Heroku~~ / __KubernetesCluster__
* [x] Zertifikat: HTTPS