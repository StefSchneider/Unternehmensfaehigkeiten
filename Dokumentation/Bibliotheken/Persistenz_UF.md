Die Bibliothek API_UF enthält alle Klassen und Methoden zur Steuerung des Speicherzugriffs.

# Klassen

## Crud_Rueckmeldung

### Methoden

#### --init--

#### ermittle_speicherinhalt_daten_lese

#### ermittle_anzahl_speicherobjekte_nutzer_lese

#### ermittle_status_objekt_nutzer_lese

#### ermittle_status_suchschluessel_nutzer_lese

#### ermittle_laenge_liste_speicherobjekte_nutzer_lese

#### ermittle_startobjekt_nutzer_lese

#### ermittle_zugriffsberechtigung_nutzer_lese
Gibt zurück, ob der Nutzer auf das Datenobjekt zugreifen darf

#### ermittle_status_daten_nutzer_lese
Gibt "Daten sind nicht mehr aktuell" zurück, wenn diese während des Zugriffs verändert wurden.

#### ermittle_speicherart_entwickler_lese
z.B. Speicher, Datei, Datenbank

#### ermittle_laenge_daten_bytes_entwickler_lese

#### ermittle_verarbeitungszeit_entwickler_lese

#### ermittle_datenstruktur_entwickler_lese

#### ermittle_strukturtiefe_baum_entwickler_lese

#### ermittle_datentyp_rueckgabeobjekt_programm_lese


## Persistenz

### Methoden


Transformation REST in CRUD: ![Uebertragung REST zu CRUD](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_Uebertragung_REST_ZU_CRUD.png)


#### --init--

#### zerlege_pfad

#### erzeuge_schluessel_neueintrag

#### zeige_datenspeicher_json

#### ersetze_letzen_schluessel

### Methoden zur Umsetzung der vier CRUD-Verben Create, Read, Update und Delete

#### erzeuge_speicherinhalt

#### lese_speicherinhalt

#### aendere_speicherinhalt

#### loesche_speicherinhalt

### Methoden zur Transformation der REST-Verben in die CRUD-Verben
-> abrufen in Transformationsmethode, ob JSON geliefert wurde

#### get_request_in_crud

#### post_request_in_crud

#### put_request_in_crud

#### patch_request_in_crud

#### delete_request_in_crud


