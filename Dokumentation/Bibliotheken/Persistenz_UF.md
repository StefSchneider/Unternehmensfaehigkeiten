Die Bibliothek Persistenz_UF enthält alle Klassen und Methoden zur Steuerung des Speicherzugriffs.


# Architektur

Die Persistenz *Hauptspeicher* wird in Form eines **Baums** aufgebaut. Dabei bildet der Microservice, zum Beispiel „prints“ die Wurzel. Sie ist gleichzeitig die Hierarchie 0.
Jede neue Ressource wird in Form eines **Knotens** in den Hauptspeicher aufgenommen. Handelt es sich bei der neuen Ressource um eine Unterressource einer bestehenden Ressource,
wird eine Eltern-Kind-Beziehung hergestellt: Der bestehende Knoten wird als **Eltern** bezeichnet, die neue Ressource (Knoten) als **Kind**. Bis auf die Wurzel und die Kinder auf der 
untersten Hierarchiestufe, kann jeder Knoten Eltern und Kinder haben, wobei aufgrund der Konstruktion jedes Kind nur ein Elternteil haben kann. Die Wurzel hat keine Eltern; die
Kinder auf der untersten Hierarchiestufe haben keine Kinder.

Erhält erstmals ein Mitglied einer bestehenden Hierarchie ein Kind, entsteht im Baum eine neue Hierarchiestufe. Beispiel: „prints“ hat die Hierarchiestufe 0, „prints/1000_4711“ wird auf der Hierarchiestufe 1 verankert.
Die Höhe des Baums ergibt sich aus der Anzahl der Hierarchiestufen. Die Breite einer Hierarchiestufe ergibt sich aus der Anzahl ihrer Knoten; die Breite des Baums ergibt sich aus
der maximalen Breite der einzelnen Hierarchiestufen.

In jedem Knoten wird die **Nummer der Ressource** abgelegt, zum Beispiel „1000_4711“, ebenso sein Speicherinhalt. **Eltern-Knoten** speichern zusätzlich ihre Kinder in Form einer Liste ab.
**Kinder-Knoten** speichern zusätzlich Ressourcen-Nummer ihrer Eltern ab. Jedes neue Kind wird in Form eines neuen **Baums** im Elterknoten abgespeichert. 


# Klassen

## Baum


## Knoten


## Speicherinhalt




## Persistenz

### Methoden




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



