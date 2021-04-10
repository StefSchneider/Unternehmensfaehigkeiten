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

### Modell ohne Filter
```
Sender  Nachricht1, Nachricht2, Nachricht3...
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Empfänger   Nachricht1, Nachricht2, Nachricht3...
```

### Modell mit einem Filter
```
Sender      Nachricht1, Nachricht2, Nachricht3...
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Subscriber
   ↓
Filter      (Alle Nachrichten wegfiltern, deren Nummer durch 2 teilbar ist.)
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Subscriber
   ↓
Empfänger   Nachricht1, Nachricht3...
```

### Modell mit zwei Filtern nacheinander
```
Sender      Nachricht1, Nachricht2, Nachricht3...
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Subscriber
   ↓
Filter      (Alle Nachrichten wegfiltern, deren Nummer durch 2 teilbar ist.)
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Subscriber
   ↓
Filter      (Nur Nachrichten durchlassen, deren Nummer durch 3 teilbar ist.)
   ↓
Publisher
   ↓
Kanal
   ↓
Broker
   ↓
Kanal
   ↓
Subscriber
   ↓
Empfänger   Nachricht3, Nachricht9...
```

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


## Beteiligte/Klassen

***https://github.com/Thierry46/pubsub/blob/master/pubsub.py***

### Sender
Beim Sender ist die Business-Logik hinterlegt, welche Nachrichten er unter welchem Topic an welche Empfänger verschickt. 

#### Methoden 

**Topic einrichten**:
Wenn der Sender einen neuen Topic, zu dem er Nachrichten verschickt, einrichten will, weist er den Publisher an, sich
bei einem Broker für einen Kanal zum Topic anzumelden. Wenn für die Topic-Namen bestimmte Regeln gelten, müssen diese
vor der Einrichtung des neuen Topics überprüft werden.

**Nachricht versenden**:
Der Sender übergibt die zu versendende Nachricht zu dem Topic und einer Nummer, beispielsweise eine UUID, zur späteren 
Identifkation der Antwort an den Publisher. Zudem teilt er dem Publisher mit, wenn die Nachricht nicht an bestimmte 
Empfänger zugestellt werden soll.

**Topic beenden**:
Wenn der Sender keine Nachrichten mehr zu einem Topic versenden will, weist er den Publisher an, sich beim Broker für
den Kanal zum Topic abzumelden.

### Publisher
Der Publisher übernimmt die An- und Abmeldung zu einem Topic beim Broker und die Veröffentlichung der Nachrichten zu dem
Topic, die er vom Sender erhält. Eine weitere Business-Logik wird beim Publisher nicht hinterlegt.

***WIE SINNVOLL IST EINE METHODE ’BEI ALLEN BROKERN ANMELDEN’?***

#### Methoden

**Topic suchen**:
Bevor der Publisher einen neuen Topic einrichtet, überprüft er, ob bereits ein solcher Topic existiert, über den andere 
Publisher bereits Nachrichten versenden.

**beim Broker anmelden**:
Der Publisher meldet auf Anweisung des Senders bei einem Broker einen Topic, den er vom Sender erhalten hat, an. Im 
selben Moment wird der Kanal vom Publisher zum Broker aufgebaut – der Publisher liefert dem Broker den Kanal mit.
Voraussetzungen:
- Eine Prüfung vorab ergibt, dass noch kein solcher Topic existiert.

**Nachricht überprüfen**:
Bevor der Publisher die Nachricht an den Kanal sendet, überprüft er, ob die Nachricht vollständig und im richtigen
Datenformat vorliegt. Falls dies nicht der Fall ist, meldet er dem Sender zurück, dass die Nachricht nicht versendbar
ist.

**Nachricht in den Kanal senden**:
Der Publisher schickt die vom Sender erhaltene Nachricht zu dem Topic in den Kanal. 
Voraussetzungen: 
- Es konnte ein Kanal vom Publisher zum Broker aufgebaut werden.

**beim Broker abmelden**:
Der Publisher meldet sich auf Anweisung des Senders vom Kanal zu dem Topic ab. Mm gleichen Moment wird der Kanal vom 
Publisher zum Broker abgebaut. 
Voraussetzungen: 
- Der Kanal enthält keine Nachrichten mehr.

***MUSS NICHT AUCH DER BROKER GELÖSCHT WERDEN, WENN KEINE PUBLISHER MEHR NACHRICHTEN ZU DEM TOPIC SCHICKEN?***

### Kanal
Bei einem Kanal handelt es sich eine FIFO(First-IN-FIRST-OUT-Queue, in die am Ende neue Nachrichten vom Publisher 
eingespielt werden und diese vorne an den Subscriber oder den Filter weitergeleitet wird.

#### Methoden

**nehme Nachricht auf**:
Der Kanal hängt die aktuell vom Publisher übermittelte Nachricht ans Ende der Queue an.

**gebe Nachricht weiter**:
Der Kanal gibt die zu vorderst stehende Nachricht in der Queue an einen Abnehmer weiter.

**lösche Nachricht**:
Der Kanal löscht die zuletzt übermittelte Nachricht aus der Queue. 
Voraussetzungen: 
- Er erhält eine positve Rückmeldung des jeweiligen Abnehmers über den Erhalt der Nachricht.

**ermittle Anzahl Nachrichten**:
Der Kanal liefert die Anzahl der sich noch in der Queue befindlichen Nachrichten zurück. Diese Methode wird benötigt, um
einen Kanal unter der Voraussetzung zu löschen, dass er keine Nachrichten enthält, die noch nicht zugestellt wurden.

***WIE PASSEN POST-SENDER UND POST-EMPFÄNGER IN DAS KONSTRUKT?***

### POST-Sender
Der POST-Sender wird zusammen mit dem POST-Empfänger eingesetzt, um die Nachrichtenzustellung zu puffern und damit
Sender und Empfänger ein weiteres Arbeiten – unabhängig von der Zustellung – zu ermöglichen. Beim POST-Sender liegt 
auch das Fehler-Handling, wenn die Nachricht nicht direlt an den POST-Empfänger zugestellt werden kann.

#### Methoden

**sende Nachricht**:
Der POST-Sender verschickt über die REST-API per POST-Request die Nachricht an den POST-Empfänger. Wenn der POST-Sender
vom POST-Empfänger keine Empfangsbestätigung erhält, setzt ein Error-Handling ein, durch das er besipielsweise die
Nachricht nach einer bestimmten Zeit nocheinmal verschickt. 
Voraussetzungen:
- Er kennt die Adresse des POST-Empängers.

**lösche Nachricht**:
Der POST-Sender löscht die zuletzt übermittelte Nachricht. 
Voraussetzungen: 
- Er erhält eine positve Rückmeldung des jeweiligen POST-Empfängers über den Erhalt der Nachricht.

### POST-Empfänger
Der POST-Empfänger erhält vom POST-Sender die Nachricht und schickt dem POST-Sender eine Empfangsbestätigung. Dann 
leitet er die Nachricht an den Input-Kanal des Abnehmers (Broker oder Subscriber) weiter. 

#### Methoden

**Nachricht in den Kanal senden**:
Der POST-Empfänger schickt die vom POST-Sender erhaltene Nachricht zu dem Topic in den Kanal. 
Voraussetzungen: 
- Es konnte ein Kanal vom POST-Empfänger zum Broker aufgebaut werden.

***WIE PASSEN POST-SENDER UND POST-EMPFÄNGER IN DAS KONSTRUKT?***


### Broker
Der Broker bildet die Schnittstelle zwischen Sendern und Empfängern. Er leitet die von den Publishern erhaltenen 
Nachrichten an die jeweiligen Subscriber zu dem Topic weiter.

#### Methoden

**Publisher anmelden**:
Der Broker nimmt den Publisher auf dessen Anmeldung hin in den Kanal zum Topic auf. Im selben Moment wird der Kanal vom
Publisher zum Broker aufgebaut. Die Methode ist das Gegenstück zu „beim Broker anmelden“ des Publishers.

**Publisher abmelden**:
Wenn sich der Publisher auf Weisung des Senders von dem Kanal zum Topic abmeldet, meldet ihn auch der Broker ab. Im 
selben Moment werden die Kanäle zu den Subscribern zu dem Topic abgebaut. Dazu wird die Methode „Kanal abbauen“ 
aufgerufen. Die Methode ist das Gegenstück zu „beim Broker abmelden“ des Publishers.
Voraussetzungen: 
- Die Kanäle sind leer. 
- Es gibt keine weiteren Publisher, die denselben Topic nutzen. 

**Kanal abbauen**:
Mit dem Kanalabbau vom Sender zum Abnehmer wird die Queue gelöscht.
Bedingungen:
- Der Input-Kanal vom Publisher zum Broker ist abgebaut UND der Output-Kanal zum Subscriber ist leer.
- Es existiert kein Subscriber mehr zu dem Output-Kanal
- Der Subscriber hat sich abgemeldet UND der Output-Kanal zum Subscriber ist leer.
Folge: Es dürfen keine Nachrichten mehr in diesen Output-Kanal gehen, das heißt kopiert werden.

**Subscriber anmelden**:
Der Broker nimmt den Subscriber auf dessen Anmeldung hin in den Kanal zum Topic auf. Im selben Moment wird der Kanal vom
Broker zum Subscriber aufgebaut und der Broker liefert dem Subscriber den Kanal zurück. Zudem muss der Broker den neuen
Output-Kanal mit dem Input-kanal vom Publisher zum Broker verbinden. Die Methode ist Gegenstück zu „beim Broker 
anmelden“ des Subscribers.

**Nachricht transportieren**:
Der Broker muss die Nachricht, die er vom Publisher erhalten hat, für jeden Kanal zum Subscriber einmal kopieren und in
jeder Queue ans Ende stellen. Anschließend löscht er die Nachricht, die er vom Publisher erhalten hat.

**Subscriber abmelden**:
Wenn sich der Subscriber auf Weisung des Senders von dem Kanal zum Topic abmeldet, meldet ihn auch der Broker ab. 
Im selben Moment wird der Kanal vom Broker zum Subscriber abgebaut. Die Methode ist das Gegenstück zu „beim Broker 
abmelden“ des Subscribers.
Voraussetzungen:
- Der Kanal vom Broker vom Subscriber ist leer.

**alle Subscriber ermitteln**:
Der Broker ermittelt alle Subscriber, die sich beim ihm zu dem Topic angemeldet haben. 

**Rückmeldung an Publisher geben**:
Der Broker teilt dem Publisher mit, welche Subscriber er ermittelt hat. Der Publisher gibt die Information an den Sender
weiter. Die Methode wird benötigt, um dem Sender mitzuteilen, wer seine Nachrichten erhält. Somit könnte der Sender 
aussteuern, wem er bestimmte Nachrichten zukünftig zukommen lassen will und wem nicht.

### Subscriber
Der Subscriber übernimmt die An- und die Abmeldung zu einem Topic beim Broker für seinen Empfänger. Zudem leitet er 
Nachrichten, die er zu dem Topic vom Broker erhält, an den Empfänger weiter. Eine weitere Business-Logik wird 
beim Subscriber nicht hinterlegt.

***WIE SINNVOLL IST EINE METHODE ’BEI ALLEN BROKERN ANMELDEN’?***

#### Methoden

**beim Broker anmelden**:
Der Subscriber meldet sich auf Anweisung des Empfängers sich beim Broker für einen bestimmten Topic an, um die 
Nachrichten zu dem Topic zu erhalten. Sobald er sich für den Topic anmeldet, wird vom Broker der Kanal zum Subscriber 
aufgebaut.

**beim Broker abmelden**:
Der Subscriber meldet sich auf Anweisung des Empfängers sich beim Broker von einem bestimmten Topic ab, um keine 
Nachrichten zu dem Topic mehr zu erhalten. Sobald er sich für den Topic abmeldet, wird vom Broker der Kanal zum 
Subscriber abgebaut. Voraussetzung: Der Kanal ist leer. Sollte das noch nicht der Fall sein, wird erst der Kanal
geleert, bevor er abgebaut wird. Mit der Abmeldung werden aber vom Broker keine neuen Nachrichten mehr in den Kanal
eingespielt.

### Empfänger
Der Empfänger verarbeitet die vom Sender verschickte Nachricht.

#### Methoden
**für Topic anmelden**:
Der Empfänger weist den Subscriber an, sich beim Broker für einen bestimmten Topic anzumelden. Die Anweisung hierzu
erhält der Empfänger über die Config-Daten.

**Rückmeldung an Sender geben**:
Wenn der Sender eine Rückantwort anfordert, schickt der Empfänger diese direkt an ihn.
Voraussetzungen:
- Der Sender hat eine ID mitgeliefert, mit deren Hilfe er die Rückantwort des Empfängers zuordnen kann.
- Der Sender hat Daten mitgeschickt, wie er erreichbar ist.

***ERFOLGT EINE DIREKTE RÜCKANTWORT ÜBER EINEN POST-REQUEST?***

### Filter
Der Filter steuert die Weitergabe von Nachrichten von Sendern zu einem Topic an Empfänger. Er bsteht aus Eingangsteil, 
das eingehende Nachrichten aufnimmt, einem Filterteil, das Nachrichten aussortiert und einem Ausgangsteil, 
das Nachrichten ausgibt. Der Filter wird durch Config-Daten mithilfe von Bool’schen Ausdrücken erstellt. Der Filter 
wird zwischen Subscriber und Epfänger gesetzt und nutzt die übrigen Elemente des Pub/Sub-Patterns. Das heißt, ausgehende
Nachrichten gibt der Filter an einen Publisher weiter, der diese über Kanäle und einen Broker an einen Subscriber und
letztendlich einen Empfänger leitet. Filter können sowohl nacheinander als auch parallel eingesetzt werden.

#### Methoden

**baue Filter auf**:
Aus den Config-Daten wird ein Filter erstellt.

**aktiviere Filter**:
Diese Methode setzt den aufgebauten Filter ein, indem sie einen Publisher, Kanäle, POST-Sender, POST-Empfänger, Broker 
und Subscriber sowie deren Methoden nutzt, um die gefilterten Nachrichten weiterzuleiten. Nach dem Aufbau leitet der 
Filter nur die durchzulassenden Nachrichten an den jeweiligen Abnehmer weiter.
Voraussetzungen:
- Die Voraussetzungen der eingesetzten Beteiligten sind erfüllt.

**deaktiviere Filter**:
Diese Methode entfernt alle bei der Filter-Aktivierung eingesetzten Beteiligte wieder und baut auch die Kanäle ab.
Voraussetzungen:
- Die Voraussetzungen der eingesetzten Beteiligten sind erfüllt.


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
