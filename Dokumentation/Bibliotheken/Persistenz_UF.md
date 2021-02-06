Die Bibliothek Persistenz_UF enthält alle Klassen und Methoden zur Steuerung des Speicherzugriffs.


# "Backlog"

Ein "hash"-Wert eignet sich gut als UUID. Es gibt sogar eine Bibliothek für Python, "Python UUID Module to Generate 
Universally Unique Identifiers [Guide] (pynative.com)". Der Vorteil ist, dass wir mit einer echten UUID über 
Computergrenzen hinweg eindeutige Schlüssel nutzen können. Die einfache Variante mit der Sequenznummer würde hierbei 
nicht mehr funktionieren, oder zumindest nicht, wenn es schnell gehen soll.
Link: https://pynative.com/python-uuid-module-to-generate-universally-unique-identifiers/

Die UUID wird in der Persistenz erzeugt.
Es wird erst einmal nicht überprüft, ob die neue UUID schon anderweitig vergeben wurde, da die Wahrscheinlichkeit recht
gering ist. Falls zu einem späteren Zeitpunkt eine solche Überprüfung nötig wird, sollten alle UUIDs in einer separaten
Liste verwaltet (Neuaufnahme und Löschung) werden. Um die Suche zu beschleunigen können die UUIDs auch in einem AVL-Baum
verwaltet werden. Dann kann schnell ermittelt werden, ob eine Doppelung vorliegt. 

**UUID1**: Besteht aus der MAC-Adresse, einer Sequenz-Nummer und der Zeit
- Hilft uns die MAC-Adresse an anderer Stelle weiter, z.B. wenn wir wissen wollen, welcher Computer die Persistenz 
angesteuert hat?
  Wollen/dürfen wir aus Datenschutzgründen die MAC-Adresse in der UUID festgehlaten haben?
  Welche MAC-Adresse wird bei der Speicherung in der Cloud genommen?
  
**UUID4**: Vollkommen zufällig erzeugte UUID ohne Basisdaten aus dem Umfeld

**UUID3/UUID5**: Aus Basis von Basisdaten ermittelte UUID
- UUID lässt sich immer reproduzieren
- wenn wir in den Parametern den NS-Namespace aktivieren, können wir beispielsweise den Namen der Persistenz verwenden
- wenn wir in den Parametern die NS-URL aktivieren, können wir beispielsweise die URL des Request-Senders oder die URL
  der Persistenz verwenden
  
*UUIDs lassen sich auch miteinander kombinieren, z.B. uuid.uuid4(uuid.uuid1())*


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

Welche Daten müssen bei einem PATCH ausgetauscht werden?
- zu beachten: Das Speicherobjekt ist bereits vorhanden 
- zu klären: alle nicht zu ändernden Speicherelemente behalten ihre UDID oder bekommen auch sie eine neue UDID?  
- alle zu ändernden Speicherelemente werden mit einem neuen UDID, ihrem Schlüssel und ihrem Speicherinhalt neu eingefügt
- alle zu ändernden Speicherinhalte erhalten als Eltern die UDID des Speicherobjekts
- alle neuen Speicherinhalte 

#### loesche_speicherinhalt

### Methoden zur Transformation der REST-Verben in die CRUD-Verben
-> abrufen in Transformationsmethode, ob JSON geliefert wurde



