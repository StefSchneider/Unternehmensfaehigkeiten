# Pub/Sub-Pattern

Pub/Sub (publish-subscribe) ist ein Nachrichten-System, in dem Sender ihre Nachrichten nicht direkt an Empfänger 
schicken, sondern über Broker zur Verfügung stellen. Dazu bedienen sie sich sogenannten Publishern und Subscribern sowie
Kanälen. Die Publisher sorgen dafür, dass die Nachrichten des Sendern zu einen bestimmten Thema (Topic) über einen Kanal
an einen Broker gesendet werden; bei diesem Broker melden sich dann die Subscriber für bestimmte Nachrichten an. Der 
Broker übermittelt dann die Nachrichten über einen Kanal an die Subscriber, die die Nachrichten an die Empfänger 
weitergeben. Bei Pub/Sub können dadurch beliebig viele Subscriber auf einen Nachrichtenkanal zugreifen, ebenso können 
beliebig viele Publisher in einen Nachrichtenkanal schreiben. Zusätzliche Filter können nur bestimmten Nachrichten, die 
über die Kanäle geschickt werden, durchlassen. Sowohl Sender als Empfänger sollen unabhängig voneinander arbeiten 
können. Der Broker sorgt dafür, dass der Sendern den oder die Empfänger nicht kennen muss, ebenso ist dem Empfänger
unbekannt, wer die Nachrichten verschickt. Für den Topic werden eigene Kanäle aufgebaut

## Modelle

![Pub/Sub Modell 1](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_API_1.png)

Das Modell ist gekennzeichnet durch: **1 Sender - 1 Topic - 1 Empfänger**

Bei dieserm Grundmodell übergibt der **Sender** seine Nachricht an einen **Publisher**, der diese über einen **Kanal** 
an einen **Broker** weiterleitet. Dieser Broker übermittelt die Nachrichten an den oder die **Subscriber**, die sich für 
den jeweiligen **Topic** angemeldet haben. Diese Subscriber geben die Nachrichten an die jeweiligen **Empfänger** 
weiter, wo sie verarbeitet werden. Damit der Sender unabhängig von Empfängern arbeiten kann und nicht darauf warten 
muss, ob es einen Empfänger gibt und wie dieser arbeitet, werden eine **Queue (Kanal)** und ein **Post-Sender** 
eingesetzt. Der Publisher gibt die Nachrichten über den Kanal an den Post-Sender, der diese an einen **Post-Empfänger** 
weiterleitet und auf entsprechende Rückmeldungen wartet - der Post-Sender kann auch Nachrichten bei einer erfolglosen 
Zustellung an den Post-Empfänger nochmals verschicken, ohne dass der Sender in seiner Arbeit beeinflusst wird. Selbst 
wenn es gar keinen Empänger gibt kann er weiterarbeiten










## Beteiligte








# Struktur






Sender->publisher->kanal->broker->kanal->subscriber->empfänger
nachricht1, nachricht2, ...                          nachricht1, nachtricht2
 
Sender->publisher->kanal->broker->kanal->subscriber->filter->publisher->kanal->broker->kanal->subscriber->empfänger
nachricht1, nachricht2, nachricht3, ...              alle geraden Nachrichten wegfiltern      nachricht1, nachricht3, ...

Sender->publisher->kanal->broker->kanal->subscriber->filter->publisher->kanal->broker->kanal->subscriber->filter->publisher->kanal->broker->kanal->subscriber->empfänger
nachricht1, nachricht2, nachricht3, ...              alle geraden Nachrichten wegfiltern                  durch 3 teilbar                          nachricht3, nachtricht9, ...

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
Folge: es dürfen keine Nachrichten mehr in diesen Output-Kanal gehen, d.h. kopiert werden

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
