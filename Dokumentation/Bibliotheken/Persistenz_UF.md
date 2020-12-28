Die Bibliothek Persistenz_UF enthält alle Klassen und Methoden zur Steuerung des Speicherzugriffs.


# Architektur

Die Persistenz *Hauptspeicher* wird in Form eines **Baums** aufgebaut. Dabei bildet der Microservice, zum Beispiel 
„prints“ die Wurzel. Sie ist gleichzeitig die Hierarchie 0. Jede neue Ressource wird in Form eines Baums in den 
Hauptspeicher aufgenommen, auch als **Knoten** bezeichnet. Handelt es sich bei der neuen Ressource um eine 
Unterressource einer bestehenden Ressource, wird eine Eltern-Kind-Beziehung hergestellt: Das bestehende Speicherelement 
wird als **Eltern** bezeichnet, die neue Ressource (Speichrelement) als **Kind**. Bis auf die Wurzel und die Kinder auf 
der untersten Hierarchiestufe, kann jedes Speicherelement Eltern und Kinder haben, wobei aufgrund der Konstruktion jedes
Kind nur ein Elternteil haben kann. Die Wurzel hat keine Eltern; die Speicherelement auf der untersten Hierarchiestufe 
haben keine Kinder.

Zur Umsetzung werden drei Klassen eingeführt: **Baum**, **Speicherelement** und **Speicherinhalt**. Jede neue Ressource
wird als neuer Baum in die Persistenz eingebunden. 

![Klassen](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_Bestandteile_Persistenz.png)

Jeder **Baum** besteht aus drei Bestandteilen:
1. Speicherelement
2. Kinder
3. Elternpfad

Im **Speicherelement** werden die abgespeicherten Daten zu der Ressource hinterlegt. Es besteht aus dem **Schlüssel** 
und dem **Speicherinhalt**. **Kinder** ist eine Liste, in der die Unterressourcen zu der aktuellen Ressource abgelegt
werden. Hat die Ressource keine Unterressourcen, bleibt die Kinderliste leer. Neue Unterressourcen (Kinder) werden als
Baum-Objekte in der Kinder-Liste abgespeichert. Der **Elternpfad** enthält ebenfalls eine Liste. Dort werden die Namen
der einzelnen Hierarchien bis zur aktuellen Ressource abgelegt, bespielsweise ["prints", "1000_4711"]. Eine solche 
Vorgehensweise erleichtert die spätere Umwandlung des Baums in ein Dictionary (siehe Docstring Methode 
*wandle_baum_in_dict*.

Jedes **Speicherelement** besteht aus zwei Betandteilen:
1. Schlüssel
2. Speicherinhalt

Unter dem **Schlüssel** wird der Name der Ressource abgelegt, zum Beispiel „1000_4711“. Unter **Speicherinhalt** sind 
die Daten zu der Ressource erfasst. 

Die Klasse **Speicherinhalt** erfasst die **Speicherdaten** als Dictionary. Eine solche Abtrennung des Speicherinhalts
als eigene Klasse erleichtert den späteren Suchalgorithmus innerhalb des Dictionaries.

Erhält erstmals ein Mitglied einer bestehenden Hierarchie ein Kind, entsteht im Baum eine neue Hierarchiestufe. 
Beispiel: „prints“ hat die Hierarchiestufe 0, „prints/1000_4711“ wird auf der Hierarchiestufe 1 verankert.
Die Höhe des Baums ergibt sich aus der Anzahl der Hierarchiestufen. Die Breite einer Hierarchiestufe ergibt sich aus der
Anzahl ihrer Knoten; die Breite des Baums ergibt sich aus der maximalen Breite der einzelnen Hierarchiestufen.

![Beispiel für Speicheraufbau](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_Aufbau_Persistenz_Datenspeicher.png)


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



