Die Bibliothek API_UF enthält alle Klassen und Methoden zur Steuerung der REST-API.

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


#### ermittle_status_objekt_nutzer_get
Gibt zurück, ob das Datenobjekt vorhanden ist oder nicht.


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
Der Aufruf der Methode erzeugt eine neue Instanz der Klasse API.
##### Parameter
***get_request_zulassen***: steuert, ob die Instanz GET-Requests entgegen nehmen darf; standardmäßig nicht
***post_request_zulassen***: steuert, ob die Instanz POST-Requests entgegen nehmen darf; standardmäßig nicht
***put_request_zulassen***: steuert, ob die Instanz PUT-Requests entgegen nehmen darf; standardmäßig nicht
***patch_request_zulassen***: steuert, ob die Instanz PATCH-Requests entgegen nehmen darf; standardmäßig nicht
***delete_request_zulassen***: steuert, ob die Instanz DELETE-Requests entgegen nehmen darf; standardmäßig nicht
##### Rückgabewerte
keine
##### Beschreibung
Bei der Instanzierung wird direkt festgelegt, welche REST-Verben für die Klasse überhaupt zugelassen werdden. Dies
erfolgt durch das setzen der Parameter für jedes REST-Verb. Die Standardeinstellung dafür ist 'False', sodass erlaubte
Verben aktiv zugeschaltet, d.h. auf 'True' gesetzt werden müssen.

#### __encode_daten
Die Methode wandelt ein Dictionary in Daten vom Typ-JSON-String um.
##### Parameter
***encode_daten_ein***: eingehendes Dictionary, das in das JSON-Format umgewandelt werden soll
##### Rückgabewerte
***__encode_daten_aus***: in JSON umgewandelte Daten
##### Beschreibung
Zur Umwandung des Datentyps wird ein JSONEncoder()-Objekt erzeugt. Zu einem späteren Zeitpunkt könnten die Daten auch in
andere Datenformate encodiert werden. Auf eine Sortierung der Daten nach Schlüsselnamen wird an dieser Stelle bewusst
verzichtet, da die API-Methoden ausschließlch dem Transport der Daten dienen.

#### __decode_daten
Die Methode wandelt die Daten vom Typ-JSON-String in ein Dictionary um.
##### Parameter
***decode_daten_ein***: eingehende Daten, die zunächst von den Request-Methoden entgegengenommen wurden und decodiert
werden sollen.
##### Rückgabewerte
***__decode_daten_aus***: in ein Dictionary umgewandelte Daten
##### Beschreibung
Zur Umwandung des Datentyps wird ein JSONDecoder()-Objekt erzeugt. Zu einem späteren Zeitpunkt könnten auch andere 
Datenformate entgegengenommen werden und decodiert werden.

### Methoden zum Empfangen von Daten
Die Methoden werden eingesetzt, um eingehende Daten durch die verschiedenen Requests zu verarbeiten. Wird beispielsweise
eine Ressource mit einem POST-Request angesprochen, werden die eingehenden Daten von der Methode **post** entgegen
genommen und verarbeitet. Die Methodennamen entsprechen den REST-Verben. Alle Daten werden im JSON-Format übertragen.

#### get
Die Methode dient der Verarbeitung eingehender Daten eines GET-Requests.
##### Parameter
***uebergabedaten_get_ein***: eingehende Daten des GET-Requests
##### Rückgabewerte
***__uebergabedaten_get_aus***: (bearbeitete) Daten des GET-Requests
##### Beschreibung
Derzeit erfolgt keine weitere Verarbeitung der Eingangsdaten, sodass diese in unveränderter Form ausgegeben werden.

#### post
Die Methode dient der Verarbeitung eingehender Daten eines POST-Requests.
#####Parameter
***uebergabedaten_post_ein***: eingehende Daten des POST-Requests
##### Rückgabewerte
***__uebergabedaten_post_aus***: bearbeitete Daten des POST-Requests
##### Beschreibung
Die eingehenden Daten werden mithilfe der Methode **decode** in ein Dictionary umgewandelt.

#### put
Die Methode dient der Verarbeitung eingehender Daten eines PUT-Requests.
#####Parameter
***uebergabedaten_put_ein***: eingehende Daten des PUT-Requests
##### Rückgabewerte
***__uebergabedaten_put_aus***: bearbeitete Daten des PUT-Requests
##### Beschreibung
Die eingehenden Daten werden mithilfe der Methode **decode** in ein Dictionary umgewandelt.

#### patch
Die Methode dient der Verarbeitung eingehender Daten eines PATCH-Requests.
#####Parameter
***uebergabedaten_patch_ein***: eingehende Daten des PATCH-Requests
##### Rückgabewerte
***__uebergabedaten_patch_aus***: bearbeitete Daten des PATCH-Requests
##### Beschreibung
Die eingehenden Daten werden mithilfe der Methode **decode** in ein Dictionary umgewandelt.

#### delete
Die Methode dient der Verarbeitung eingehender Daten eines DELETE-Requests.
#####Parameter
***uebergabedaten_delete_ein***: eingehende Daten des DELETE-Requests
##### Rückgabewerte
***__uebergabedaten_delete_aus***: bearbeitete Daten des DELETE-Requests
##### Beschreibung
Die eingehenden Daten werden mithilfe der Methode **decode** in ein Dictionary umgewandelt.

### Methoden zum Senden von Daten

#### hole


#### schreibe


#### ueberschreibe


#### aendere


#### loesche

