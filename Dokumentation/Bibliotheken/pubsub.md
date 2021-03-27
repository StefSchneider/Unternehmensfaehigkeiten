# Pub/Sub-Pattern

Pub/Sub (publish-subscribe) ist ein Nachrichten-System, in dem **Sender** ihre Nachrichten nicht direkt an **Empfänger** 
schicken, sondern über einen **Broker** zur Verfügung stellen. Dazu bedienen sie sich sogenannten **Publishern** und 
**Subscribern** sowie **Kanälen**. Die Publisher sorgen dafür, dass die Nachrichten des Senders zu einem bestimmten 
**Topic** (Thema) über einen Kanal (Ausgangskanal) an einen Broker gesendet werden; bei diesem Broker melden sich dann 
die Subscriber für bestimmte Topics an. Der Broker übermittelt dann die Nachrichten zu dem Topic über jeweils einen 
Kanal (Eingangskanal) an die Subscriber, die die Nachrichten an die **Empfänger** weitergeben. 

![Pub/Sub Grundmuster](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Grundmuster.png)

Bei Pub/Sub können dadurch beliebig viele Subscriber auf einen Nachrichtenkanal zugreifen, ebenso können 
beliebig viele Publisher in einen Nachrichtenkanal schreiben. Zusätzliche Filter können nur bestimmten Nachrichten, die 
über die Kanäle geschickt werden, durchlassen. Sowohl Sender als Empfänger sollen unabhängig voneinander arbeiten 
können. Der Broker sorgt dafür, dass der Sender den oder die Empfänger nicht kennen muss, ebenso ist dem Empfänger
unbekannt, wer die Nachrichten verschickt. Für jeden Topic wird ein eigener Pub/Sub-Service aufgebaut. 

Diese asynchrone Verarbeitung der Nachrichten sorgt dafür, dass das Gesamtkonstrukt nicht durch Probleme einzelner 
Bereiche blockiert wird.

## Modelle

![Pub/Sub Modell 1](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Modell_1.png)

Das Modell ist gekennzeichnet durch: **1 Sender - 1 Topic - 1 Empfänger**

Bei dieserm **Grundmodell* übergibt der **Sender** seine Nachricht an einen **Publisher**, der diese über einen 
**Kanal** (Ausgangskanal) an einen **Broker** weiterleitet. Dieser Broker übermittelt die Nachrichten über einen 
weiteren Kanal (Eingangskanal) an den **Subscriber**, der sich für den jeweiligen **Topic** angemeldet hat. Der 
Subscriber geben die Nachrichten an die jeweiligen **Empfänger** weiter, wo sie verarbeitet werden. 

Damit der Sender unabhängig von Empfängern bzw. dem Broker arbeiten kann und nicht darauf warten muss, ob es einen 
Empfänger gibt und wie dieser arbeitet, werden eine **Queue (Kanal)** und ein **POST-Sender** eingesetzt. Der Publisher 
gibt die Nachrichten über den Kanal an den POST-Sender, der diese an einen **POST-Empfänger** weiterleitet und auf 
entsprechende Rückmeldungen wartet – der POST-Sender kann auch Nachrichten bei einer erfolglosen Zustellung an den 
POST-Empfänger nochmals verschicken, ohne dass der Sender in seiner Arbeit beeinflusst wird. Selbst wenn es gar keinen 
Empfänger gibt, kann er weiterarbeiten. Die gleiche Struktur mit Post-Sender und Post-Empfänger wird auch auf dem Weg 
vom Broker zum Subscriber angewendet. Damit dient das Konstrukt POST-Sender/POST-Empfänger quasi als Puffer,

![Pub/Sub Modell 2](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Modell_2.png)

Das Modell ist gekennzeichnet durch: **2 Sender - 2 Topics - 2 Empfänger**

Im Vergleich zu **Modell 1** gibt es hierbei unterschiedliche Topics, unter denen Sender Nachrichten senden, ebenso 
gibt es mehrere Empfänger, für diese Nachrichten interessanr sind. Da zwei Topics von unterschiedlichen Sendern gesetzt 
und Empfängern bezogen werden, können beide Systeme vollkommen unabhängig voneinander agieren.

![Pub/Sub Modell 3](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Modell_3.png)

Das Modell ist gekennzeichnet durch: **1 Sender - 1 Topic - 2 Empfänger**

Meldet sich mehr als ein Subscriber für einen Topic an, baut der Broker zu jedem Subscriber einen eigenen Kanal auf. 
Damit vermeidezt er, dass die anderen Empfänger die Nachrichten zu dem Topic nicht erhalten, wenn ein Empfänger 
ausfällt oder die Zustellung verzögert wird.

![Pub/Sub Modell 4](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Modell_4.png)

Das Modell ist gekennzeichnet durch: **1 Sender - 2 Topics – jeweils 1 Empfänger**

Bei diesem Modell verschickt der Sender Nachrichten zu unterschiedlichen Topics. Für jeden Topic nutzt er einen eigenen 
Pub/Sub-Service mit eigenem Publisher, Kanal und Broker. In diesem Modell hat zudem jeder Topic auch zwei Empfänger.


![Pub/Sub Modell 5](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Modell_5.png)

Das Modell ist gekennzeichnet durch: **2 Sender - 1 Topic - 2 Empfänger**

Hierbei verschicken mehrere Sender Nachrichten zum gleichen Topic. Um sich nicht gegenseitig zu behinder, baut jeder 
Sender über einen Publisher einen Kanal zu dem Broker auf, der Nachrichten zu diesem Topic steuert. Ebenso baut der 
Broker einen eigenen Kanal zu jedem Subscriber auf (siehe Modell 2 und Modell 3).

## Filter

**Filter** dienen dazu, nur bestimmte Nachrichten an die Subscriber und damit an die Empfänger durchzulassen. Jeder 
Filter hat einen Eingangsteil und einen Ausgangsteil. Zwischen diesen beiden Teilen werden Nachrichten ausgesteuert. 

![Pub/Sub Filtereinsatz](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Filtereinsatz.png)

Um einen Filter in ein Pub/Sub-System einzusetzen, wird die Fuktionsweise des Grundmodells benutzt. So agiert der Filter
als Empfänger, der sich über einen Subscriber bei einem Broker für Nachrichten zu dem entsprechenden Topic anmeldet. 
Erhält der Filter auf diesem Weg Nachrichten, steuert er sie entsprechende der Regeln aus oder leitet sie weiter. Dazu
nutzt er ebenfalls einen eigenen Broker und einen eigenen Ausgangskanal. Der Broker leitet die Nachrichten über den
Eingangskanal an den Subscriber weiter, der diese an den eigentlichen Empfänger übergibt.

Auch für den Einsatz der Filter wird der Puffer üder das Konstrukt POST-Sender/POST-Empfänger verwendet. Dabei werden 
ein POST-Empfänger und ein Kanal vor den Filter gesetzt. Den Schluss des Filtereinsatzes bildet ein Kanal und ein
POST-Sender, der wiederum die Nachricht an einen anderen POST-Empfänger übergibt.

Mit dieser Konstruktion können beliebig viele Filter hintereinander oder auch parallel eingesetzt werden.

Sender → Publisher → Kanal → Broker → Kanal → Subscriber → Empfänger
Nachricht1, Nachricht2, ...                                Nachricht1, Nachtricht2, ...
 
Sender → Publisher → Kanal → Broker → Kanal → Subscriber → Filter → Publisher → Kanal → Broker → Kanal → Subscriber → Empfänger
Nachricht1, Nachricht2, Nachricht3, ...                    Alle Nachrichten wegfiltern,                               Nachricht1, Nachricht3, ...
                                                           deren Nummer durch 2 teilbar ist. 

Sender → Publisher → Kanal → Broker → Kanal → Subscriber → Filter → Publisher → Kanal → Broker → Kanal → Subscriber → Filter → Publisher → Kanal → Broker → Kanal → Subscriber → Empfänger
Nachricht1, Nachricht2, Nachricht3, ...                    Alle Nachrichten wegfiltern,                               Nur Nachrichten durchlassen,                               Nachricht3, Nachtricht9, ...
                                                           deren Nummer durch 2 teilbar ist.                          deren Nummer durch 3 teilbar ist.

## Schnittstellen

![Pub/Sub Schnittstellen](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafiken/Pub_Sub_Schnittstellen.png)

Zur Übergabe der Nachrichten (Daten) an die Beteiligten werden folgende Schnittstellen genutzt:
- Sender → Subscriber: definierte API
- Subscriber → Ausgangskanal: REST
- Ausgangskanal → POST-Sender: REST
- POST-Sender → POST-Empfänger: REST
- POST-Empfänger → Ausgangskanal: REST
- Ausgangskanal → Broker: REST
- Broker → Eingangskanal: REST
- Eingangskanal → POST-Sender: REST
- POST-Sender → POST-Empfänger: REST
- POST-Empfänger → Eingangskanal: REST
- Eingangskanal → Subscriber: REST
- Subscriber → Empfänger: definierte API





## Beteiligte

### Sender

#### 






# Struktur








sender->publisher->kanal

kanal->subscriber->empfänger

->filter->subscriber

filter besteht aus publisher und kanal

filter ist auf der einen Seite der Empfänger und auf der anderen Seite (nach der Filterung) der Sender

# Beteiligte

## Broker

### Methoden

#### Publisher anmelden
Gegenstück zu "beim Broker anmelden" des Publishers

#### Publisher abmelden
Gegenstück zu "beim Broker abmelden" des Publishers
im gleichen Moment werden die Kanäle zu den Subscribern abgebaut (erst wenn der Kanal leer ist)
Funktion "Kanal abbauen" aufrufen

#### Kanal abbauen
Bedingungen:
- Der Input-Kanal vom Publisher zum Broker ist abgebaut UND der Output-Kanal zum Subscriber ist leer
- Es existiert kein Subscriber mehr zu dem Output-Kanal
- Der Subscriber hat sich abgemeldet UND der Output-Kanal zu Subscriber ist leer
Folge: Es dürfen keine Nachrichten mehr in diesen Output-Kanal gehen, d.h. kopiert werden

#### Subscriber anmelden
Gegenstück zu "beim Broker anmelden" des Subscribers
im gleichen Moment wird der Kanal vom Broker zum Subscriber aufgebaut
liefert dem Subscriber den Kanal zurück
muss den Kanal mit dem Input-Kanal vom Publisher zum Broker verbinden

#### Nachricht transportieren
muss Nachricht, die er vom Publisher erhalten hat, für jeden Kanal zum Subscriber einmal kopieren
löscht anschließend die Nachricht, die er vom Publisher erhalten hat

#### Subscriber abmelden
Gegenstück zu "beim Broker abmelden" des Subscribers
im gleichen Moment wird der Kanal vom Broker zum Subscriber abgebaut, aber erst, wenn der Kanal leer ist 

#### alle Subscriber ermitteln

#### Rückmeldung an Publisher geben

## Publisher

### Methoden

#### beim Broker anmelden
im gleichen Moment wird der Kanal vom Publisher zum Broker aufgebaut und liefert dem Broker den Kanal mit

#### Nachricht in den Kanal senden
Voraussetzung: Es konnte ein Kanal vom Publisher zum Broker aufgebaut werden

#### beim Broker abmelden
im gleichen Moment wird der Kanal vom Publisher zum Broker abgebaut

## Subscriber

### Methoden

#### beim Broker anmelden
im gleichen Moment wird der Kanal vom Broker zum Subscriber aufgebaut

#### beim Broker abmelden
im gleichen Moment wird der Kanal vom Broker zum Subscriber abgebaut, Voraussetzung: Der Kanal ist leer

## Sender

### Methoden

## Empfänger

### Methoden

## Filter
Filters: Filters are Boolean expressions that are executed against the messages for a specific topic or topic group.

### Methoden

#### Filter aufbauen

#### Filter verändern

#### Filter abbauen

## Klassen

### Kanal

### Broker

### Subscriber

### Publisher

### Filter

## Umsetzung

### Programme

Der Prozess wird im Grundmodell in drei Programme zerlegt:
- Programm 1: Sender bis einschließlich POST-Sender
- Programm 2: POST-Empfänger bis einschließlich POST-Sender
- Programm 3: POST-Empfänger bis einschließlich Empfänger

### Objekte

Für folgende Beteiligte werden Objekte instanziert:
- Sender
- Publisher
- Kanal
- POST-Empfänger
- Broker
- Subscriber
- Empfänger
- Filter

### Klassen

#### Sender

##### Methoden


#### Publisher

##### Methoden


#### Kanal

##### Methoden


#### POST_Sender

##### Methoden


#### POST_Empfaenger

##### Methoden


#### Broker

##### Methoden


#### Subscriber

##### Methoden


#### Empfaenger

##### Methoden


#### Filter

##### Methoden

