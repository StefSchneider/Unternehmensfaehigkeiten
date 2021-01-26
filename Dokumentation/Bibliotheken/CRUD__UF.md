


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
Die Methode ermittelt die Verarbeitungszeit des Speicherzugriffs.
##### Parameter
***startzeit***: Die Startzeit überträgt die ermittelte Startzeit in die Methode. Sie dient der Berechnung der Verarbeitungszeit. Stanardmäßig wird der Parameter auf -1 gesetzt.
##### Rückgabewerte
***startzeit***: Ermittelte Startzeit des Speicherzugriffs.

***endzeit***: Ermittelte Endzeit des Speicherzugriffs.

***verarbeitungszeit:*** Differenz zwischen Endzeit und Startzeit.
##### Beschreibung
Die Methode wird sowohl kurz vor dem Start des Speicherzugriffs aus auch direkt nach seinem Ende aufgerufen. Wird der Parameter *startzeit* (= -1) nicht verändert, wird die ermittelte Zeit der *startzeit* zugewiesen. 
Wird die *startzeit* als Parameter mitgeliefert, so wird die ermittelte Zeit der *endzeit* zugewiesen und es erfolgt eine Berechnung der Differenz, die als *verarbeitungszeit* zurückgeliefert wird.
Zur Ermittlung von *startzeit* und *endzeit* wird der Microservice **ms_zeitstempel** aufgerufen.

#### ermittle_datenstruktur_entwickler_lese

#### ermittle_strukturtiefe_baum_entwickler_lese

#### ermittle_datentyp_rueckgabeobjekt_programm_lese

Transformation REST in CRUD: ![Uebertragung REST zu CRUD](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_Uebertragung_REST_ZU_CRUD.png)


#### get_request_in_crud

##### Parameter

##### Rückgabewerte

##### Beschreibung


#### post_request_in_crud

##### Parameter

##### Rückgabewerte

##### Beschreibung


#### put_request_in_crud

##### Parameter

##### Rückgabewerte

##### Beschreibung


#### patch_request_in_crud

##### Parameter

##### Rückgabewerte

##### Beschreibung
In dem wie wir jetzt die Tabellen gestaltet haben wäre jedoch die Variante, dass nur die geänderten Element neu angelegt 
werden zu weniger "Datenmüll" führt. In jedem Fall sind sowohl beim Elternelement das/die UUID(s) der neuen Kind(er) zu 
referenzieren als auch bei dem/den neuen Kind(ern) der jeweilige UUI des Elternelements.


#### delete_request_in_crud

##### Parameter

##### Rückgabewerte

##### Beschreibung
