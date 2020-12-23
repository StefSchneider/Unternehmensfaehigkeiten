



# Umgang mit Daten/Namen in Methoden

## Bennenung von Parametern/Variablen
- **eingehende Parameter**: normales sprechende Benamung 
- **lokale Variablen aus eingehenden Parametern**: Ergänzung des Namens mit Suffix "_ein". Beispiel: __ebenen_ein 
- **lokale Variablen**: Ergänzung des Namens mit Prefix "__" zur Kennzeichnung, dass es sich um eine private Variable handelt
- **Rückgabedaten**: Ergänzung des Namens mit Suffix "_aus". Beispiel: __daten_patch_aus

## Annotation
- **Parameter in Methodenköpfen**: werden mit einer Typ-Annotation versehen
- **lokale Variablen**: werden mit einer Typ-Annotation versehen, auch wenn sie aus eingehenden Parametern übernommen werden
- **globale Variablen**: werden mit einer Typ-Annotation versehen

## Vorgehen bei Berechnungen mit Variablen
1. Übernahme der Parameter in lokale Variablen. Beispiel: Parameter "ebenen" wird zu lokaler Variable "__ebenen_ein"
2. Die Parameter werden in der gleichen Reihenfolge wie im Methodenkopf in lokale Variablen überführt 
3. Alle Variablen werden zu Beginn der Methode initialisiert
4. Berechnungen auf Basis der lokalen Variablen erfolgen in anderen Variablen. Bespiel: __anzahl_ebenen = len(__ebenen_ein)
5. Der Datentyp einer Varablen darf nicht verändert werden - statdessen erfolgt die Veränderung in einer neuen Variablen



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

