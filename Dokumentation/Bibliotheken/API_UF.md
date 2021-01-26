Die Bibliothek API_UF enthält alle Klassen und Methoden zur Steuerung der REST-API. Dies betrifft Methoden zum Senden
oder Empfangen von Daten sowie Methoden, um das Senden und Empfangen vorzubereiten.

# Änderungen und Ergänzungen im Vergleich zum bisherigen Stand:
- Hinzufügen Methode zur Übersetzung JSON-String in Tabellen - zu klären: Mit welcher Routine erfolgt das Auslesen des 
  JSON-String, d.h. wie müssen die Daten angeordnet sein?`
- Bereich REST-Rueckmeldung evtl. auslagern




# Klassen

## API
Die Klasse umfasst alle Methoden, die für den Aufruf der Schnittstelle benötigt werden. Die Methoden teilen sich auf in:
- grundsätzliche Methoden, Hilfsmethoden zur Verarbeitung der Daten,
- Methoden zum Empfangen der Daten über die Schnittstelle,
- Methoden zum Senden der Daten über die Schnittstelle.

Die Namen der Methoden zum Empfang von Daten entsprechen denen der REST-Verben, die Namen der Methoden zum Senden von 
Daten haben adäquate deutsche Namen.

![Einsatz von Methoden](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_API_1.png)

Bei der Ausführung eines Requests wird die Bibliothek API sowohl vom Request-Sender als auch vom Request-Empänger 
aufgerufen. Der Request-Sender ruft die entsprechende Methode zum senden eines Requests auf: **hole()**, **schreibe()**, 
**überschreibe()**, **aendere()** oder **loesche()**. Der Request-Empfänger ruft die entsprechende Gegenmethode auf: 
**get()**, **post()**, **put**, **patch** oder **delete**.

Request: GET -> Methode Sender: hole() -> Methode Empänger: get()

Request: POST -> Methode Sender: schreibe() -> Methode Empänger: post()

Request: PUT -> Methode Sender: ueberschreibe() -> Methode Empänger: put()

Request: PATCH -> Methode Sender: aendere() -> Methode Empänger: patch()

Request: DELETE -> Methode Sender: loesche() -> Methode Empänger: delete()


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
Die Methode wandelt ein Dictionary in Daten vom Typ Bytes um.
##### Parameter
***uebergabedaten***: eingehendes Dictionary, das in das Bytes-Format umgewandelt werden soll
##### Rückgabewerte
***__uebergabedaten_encode***: in Bytes umgewandelte Daten
##### Beschreibung
Die uebergabedaten werden in einem ersten Schritt von einem Dictionary in einen JSON-String umgewandelt. In einem 
zweiten Schritt erfolgt die Umwandlung von einem JSON-String zum Datenformat Bytes. Auf eine Sortierung der Daten nach 
Schlüsselnamen wird an dieser Stelle bewusst verzichtet, da die API-Methoden ausschließlch dem Transport der Daten 
dienen.

#### __decode_daten
Die Methode wandelt die Daten vom Typ Bytes in eine Tabelle um.
##### Parameter
***uebergabedaten***: übertragene Daten, die zunächst von den Request-Methoden entgegengenommen wurden und decodiert
werden sollen.
##### Rückgabewerte
***__uebergabedaten_decode***: in eine Tabelle umgewandelte Daten
##### Beschreibung
Die uebergabedaten werden in einem ersten Schritt vom Datentyp Bytes in einen JSON-String umgewandelt. In einem 
zweiten erfolgt die Umwandlung in einen Tabelle. Dazu wird die Methode __json_in_tabelle() aufgrufen. Zu einem späteren 
Zeitpunkt könnten auch andere Datenformate, z.B. XML, entgegengenommen werden und decodiert werden. Auch dazu ruft 
__decode_daten entsprechende Umwandlungsmethoden auf. Diese hängt vom transportierten Datenformat ab.

#### __json_in_tabelle
Die Methode wandelt dien Daten vom Typ JSON-String in eine Tabelle um.
##### Parameter
***uebergabedaten***: übertragene Daten, die zunächst von Bytes in einen JSON-String umgewandelt wurden.
##### Rückgabewerte
***__ubergabedaten_tabelle***: in eine Tabelle umgewandelte Daten
##### Beschreibung
Die Methode liest die JSON-String aus und sortiert die dort enthaltenen Daten nach den Schlüsseln in eine leere Tabelle.


### Methoden zum Senden von Daten
Die Methoden werden eingesetzt, um Daten an den anfragenden Microservice zu übermitteln. So schickt die Methode 
**schreibe** Daten per POST-Request an die entsprechende Ressource. Die Namen der Methoden wurden adäquat zu den Namen
für den Empfang von Daten gewählt. Beispielsweise ist **aendere** das Pendant zu **patch**.
Alle Daten werden im JSON-Format gesendet.

#### hole
Die Methode greift per GET-Request auf eine Ressource zu und erhält das entsprechende Datenobjekt.
##### Parameter
***uebergabedaten_hole_ein***: Daten, die beim GET-Request mitgeschickt werden sollen; derzeit ohne Nutzung/Verarbeitung
##### Rückgabewerte
***__uebergabedaten_hole_aus***: Daten, die über den GET-Request auf die Ressource geliefert werden
##### Beschreibung
Die Methode startet einen GET-Request auf eine Ressource. Die erhaltenen Daten werden von der Methode im JSON-Format 
zurückgegeben.

#### schreibe
Die Methode schreibt über einen POST-Request Daten in eine Ressource.
##### Parameter
***uebergabedaten_schreibe_ein***: 
##### Rückgabewerte
***__uebergabedaten_schreibe_aus***:
##### Beschreibung

#### ueberschreibe

##### Parameter

##### Rückgabewerte

##### Beschreibung

#### aendere

##### Parameter

##### Rückgabewerte

##### Beschreibung

#### loesche

##### Parameter

##### Rückgabewerte

##### Beschreibung


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
