



# Umgang mit Daten/Namen in Methoden

## Bennenung von Parametern/Variablen
- **eingehende Parameter**: Ergänzung des Namens mit "_ein". Beispiel: daten_patch_ein
- **Rückgabedaten**: Ergänzung des Namens mit "_aus". Beispiel: daten_patch_aus

## Annotation
Neue Variablen bzw. Variablen, deren Typ sich durch Bearbeitung ändert, werden mit einer Typ-Annotation versehen.

## Bennung bei Verarbeitung
- im ersten Schritt werden die mitgegebenen Parameter in die Methode übernommen. Beispiel: __daten_post = daten_post_ein
- im zweiten Schritt werden die Berechnungen mit den übernommenen Daten durchgeführt
- in letzten Schritt werden die veränderten Daten den Ausgabedaten der Methode zugewiesen. Beispiel: __daten_post_aus = __daten_post
- return __daten_post_aus


Parameter in einer Methode werden mit einer Typ-Annotation versehen.

Alle Variablen werden mit einer Typ-Annotation versehen, auch die lokalen Variablen, die aus einem Parameter in der Methode übernommen werden

Alle Variablen werden am Anfang einer Methode initialisiert. Zuerst werden die lokalen Vriablen aus den Parametern erzeugt.






# Darstellung als Mark-Downs

"#": Oberbegriffe wie z.B. "Klassen", "Variablen", "Konstanten"

"##": Klassen-Namen

"###": Trenner "Methoden", Trenner "Attribute"

"####": Trenner "Parameter", Trenner "Beschreibung"

**fett**: Methodennamen, Objektnamen

*kursiv*: Variablen, Attribute im Text

***fett u. kursiv***: Parameter in Methodennamen im Text

'...': Wertezuweisungen

```grau hinterlegt```: Modulnamen 

