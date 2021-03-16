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
