Die Bibliothek API_UF enthällt alle Klassen und Methoden zur Steuerung der REST-API.

# Klassen

## Rest_Rueckmeldung
Die Klasse ermittelt die Daten, die an den GET-Request zurückgeliefert werden. Dabei unterscheidet sie,für wen die 
Rückgabedaten bestimmt sind: Daten (reine Daten des Speicherobjektes), Nutzer, Entwickler oder Programm. Die Daten für 
den Entwickler sollen zu- und abschaltbar sein. Datenformat der Rückgabe ist JSON.

Die Methoden werden für jedes REST-Verb programmiert, in ihrem Namen werden der jeweilige Empfänger und das jeweilige 
REST-Verb festgehalten, um einen schnelle Zuordnung zu gewährleisten. 

### Methoden

#### --init--


#### ermittle_speicherinhalt_daten_get


#### ermittle_anzahl_speicherobjekte_nutzer_get


#### ermittle_status_nutzer_get


#### ermittle_laenge_liste_speicherobjekte_nutzer_get


#### ermittle_startobjekt_nutzer_get


#### ermittle_laenge_daten_bytes_entwickler_get


#### ermittle_verarbeitungszeit_entwickler_get


#### ermittle_datenstruktur_entwickler_get


#### ermittle_strukturtiefe_baum_entwickler_get


#### ermittle_server_datenquelle_entwickler_get


#### ermittle_datentyp_rueckgabeobjekt_programm_get


#### rueckmeldung_objekte_fuellen_get


#### rueckmeldung_objekte_filtern





## API
Die Klasse umfasst alle Methoden, die für den Aufruf der Schnittstelle benötigt werden. Die Methoden teilen sich auf in:
- grundsätzliche Methoden, Hilfsmethoden zur Verarbeitung der Daten,
- Methoden zum Empfangen der Daten über die Schnittstelle,
- Methoden zum Senden der Daten über die Schnittstelle.

Die Namen der Methoden zum Empfang von Daten entsprechen denen der REST-Verben, die Namen der Methoden zum Senden von 
Daten haben adäquate deutsche Namen.

### Methoden

#### --init--


#### __encode_daten


#### __decode_daten

### Methoden zum Empfangen von Daten

#### get


#### post


#### put


#### patch


#### delete


### Methoden zum Senden von Daten

#### hole


#### schreibe


#### ueberschreibe


#### aendere


#### loesche

