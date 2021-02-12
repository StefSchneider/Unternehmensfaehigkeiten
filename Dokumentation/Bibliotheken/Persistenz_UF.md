Die Bibliothek Persistenz_UF enthält alle Klassen und Methoden zur Steuerung des Speicherzugriffs.

## Aufbau der Persistenz

Die Speicherobjekte für die jeweilige Ressource werden entweder in Form einer Datei oder einer Datenbank gespeichert.

Es werden zwei Tabellen aufgebaut - eine Tabelle für die Struktur und eine Tabelle für den Inhalt der Speicherobjekte.

#### Tabelle Inhalt
Die Inhalte-Tabelle erfasst zu jedem Speicherobjekt den Inhalt. Sie besteht aus den Spalten 
- UUID
- Schlüssel
- Speicherinhalt

#### Tabelle Struktur
Anhand der Struktur-Tabelle können die Eltern-Kind-Verbindungen innerhalb der Resource nachvollzogen werden. Sie besteht 
aus den Spalten
- UUID
- Schlüssel
- Eltern
- Kind

Die UUID bildet die Verknpüfung der Struktur-Tabelle zur Inhalte-Tabelle

## Verwendung von UUID für Speicherobjekte

Jedes Speicherobjekt erhält zur genauen Identifizierung eine UUID (Universally Unique Identifier). Die UUID ist ein
32-stelliger Zahlen-/Buchstabencode, der mit verschiedenen Mechanismen erzeugt werden kann. Die UUID wird in der 
Persistenz erzeugt, damit ist die Methode Bestandteil der Bibliothek Persistenz_UF. Zur Erzeugung der UUID werden 
Built-in-Methoden aus der Python Bibliothek uuid verwendet. 

Bei der Erzeugung der UUID wird nicht geprüft, ob genau diese UUID schon vergeben wurde, da aufgrund des Erzeugungs-
mechanismus nur eine äußerst geringe Wahrscheinlicheit besteht, dass eine bestimmte UUID mehr als einmal generiert wird
bzw. verwendet wird. 

Sollte zu einem späteren Zeitpunkt eine solche Überprüfung nötig werden, sollten alle UUIDs in einer separaten
Liste verwaltet (Neuaufnahme und Löschung) werden. Um die Suche zu beschleunigen können die UUIDs auch in einem AVL-Baum
verwaltet werden. Dann kann schnell ermittelt werden, ob eine Doppelung vorliegt. 

#### UUID-Versionen:

**UUID1**: 
- Wird aus der MAC-Adresse, einer Sequenz-Nummer und einem Zeitstempel generiert.
- Die UUID ist nicht reproduzierbar.
- Es wird immer die MAC-Adresse des Computers verwendet, auf dem sie abgespeichert wird.
- Da die MAC-Adresse Bestandteil der UUID ist, sehen Datenschützer die UUID teilweise kritisch.
- Wird häufig von SQL-Datenbanken genutzt.

**UUID3** und **UUID5**
- Wird teilweise auf Basis von vorzugebenden Parametern ermittelt, z.B. Namespace_DNS oder Namespace_URL
- Erzeugung erfolgt mit cryptografischen Methoden
_ Die UUID ist reproduzierbar.
  
**UUID4**
- Vollkommen zufällig erzeugte UUID ohne Basisdaten aus dem Umfeld
- Die UUID ist nicht reproduzierbar.
- Wird häufig von Non-SQL-Datenbanken verwendet.

**Für unsere Anwendung nutzen wir die Version UUID1.**

#### Gründe für die Entscheidung:

Mit hoher Wahrscheinlichkeit verwenden wir eine SQL-Datenbank. Dann kann die Erzeugung der UUID1 auch von der Datenbank
übernommen werden. Die Datenschutzbedenken sind nicht gerechtfertigt, da sich von der MAC-Adresse nicht unbedingt auf
den Besitzer des Computers schließen lässt. Zudem werden durch die Speicherung der Daten in der Cloud eine Vielzahl von
MAC-Adressen verwendet, was auch das Risiko eine doppelten Erzeugung einer bestimmten UUID deutlich verringert.

UUIDs der Versionen 3 und 5 kommen nicht infrage, da wir - wenn wir zum Beispiel die URL der Persistenz als Parameter
vorgeben würden -, beim Umhängen von Speicherobjekten in eine andere Persistenz neue UUIDs für die jedes umgehangene
Speicherobjekt generieren müssen.

#### Zu beachten:

Die UUID sollte nicht als String mit Hex-Zahlen dargestellt werden, sondern mit einer Integer-Zahl, da sich diese 
schneller verarbeiten lassen als Strings. Da diese Integer-Zahlen aber unterschiedlich lang sein können, müssen sie
bei einer Ausgabe eventuell formatiert werden.

Mehr Informationen zu UUIDs: 
https://pynative.com/python-uuid-module-to-generate-universally-unique-identifiers/

## Index

Neben den Tabellen, die in der Persistenz abgelegt werden, erfolgt eine Indizierung der Speicherobjekte mithilfe eines
AVL-Baums. Bei einem AVL-Baum handelt es sich um einen ausgerichteten binären Suchbaum.

Der Index wird auf Basis der Speicherinhalte aufgebaut und soll eine Suche nach Speicherinhalten beschleunigen. 

Ein Knoten des AVL-Baums besteht aus dem Inhalt zwei Zeigern - ein Zeiger auf das linke Kind und ein Zeiger auf das 
rechte Kind. Beide Kinder sind ebenfalls Knoten. Ausnahme: Sie haben keine Kinder; dann handelt es sich bei dem Knoten
um ein sogenanntes Blatt. Die Kinder sind nicht zu verwechseln mit den Kindern in der Strutur-Tabelle der Persistenz.
Der Knoteninhalt besteht aus einem Zeiger auf die Position des Speicherobjekts in der Persistenz.

### Einbindung eines neues Speicherobjekts in den Index
Wird ein neues Speicherobjekt in die Persistenz aufgenommen, wird ein entsprechender Knoten dazu auch in den AVL-Baum
gehangen. Dabei wird der Speicherinhalt des neuen Speicherobjekts mit dem Speicherinhalt der bestehenden Knoten des 
AVL-Baums verglichen, beginnend beim obersten Knoten, der sogennanten Wurzel.

Ist der Inhalt des neuen Speicherobjekts kleiner als der Inhalt des Speicherobjekts, auf den der Zeiger im Knoten 
verweist, wird im Baum nach links gegangen, das heißt das nächste Vergleichsobjekt liegt hinter dem Knoten, der das 
linke Kind ist. Ist der Inhalt des neuen Speicherobjekts hingegen größer als der Inhalt des Speicherobjekts, auf den
der Zeiger im Knoten verweist, geht der Schritt auf das rechte Kind. Diese Verglich erfolgen solange bis die richtige
Position für das neuen Knoten erreicht ist. Dort wird er als Kind eines Elternknotens in den Baum gehangen.

### Ausrichtung des Baums
AVL-Bäume kennzeichnen sicch dadurch, dass sich an jedem Knoten die Höhe der beiden Teilbäume um höchstens eins 
unterscheidet. Mit (fast) jeder Veränderung des Baums durch die Aufnahme oder Löschung eines Knotens ändern sich die
Höhenverhältnisse, sodass der Baum neu ausgerichtet werden muss. In unserem Programm wird nicht nach jeder Veränderung
gerüft, ob eine solche Rotation erfolgen muss, sondern erst nach einer bestimmten Anzahl an Veränderungen. Diese Zahl
wird für jede Persistenz festgelegt und ist veränderbar.

### Bibliothek
Zur Erzeugung und Verwaltung der AVL-Baum wird eine eigene Bibliothek AVL-Baum mit den entsprechenden Klassen und 
Methoden angelegt.


Mehr Informationen zu AVL-Bäumen:
https://de.wikipedia.org/wiki/AVL-Baum
https://www.youtube.com/watch?v=EyrMyI3HG1g

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



