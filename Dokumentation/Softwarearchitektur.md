# Allgemein
Das Projekt besteht aus einzelnen Microservices, die von jeweils anderen Microservices aufgerufen werden.
Der Datenaustausch erfolgt über eine REST Api als Schnittstelle, das bevorzugte Datenformat zum Austausch über diese 
Schnittstelle ist JSON.

# Libraries
 Zur Umsetzung werden drei verschiedene Libraries erstellt, die in die entsprechenden Microservices geladen werden:
 1. Library **Config_UF**
 2. Library **API_UF**
 3. Library **Persistenz_UF**
 
 Der Aufbau mithilfe von Libraries sorgt dafür, dass Programmteile ausgetauscht bzw. erweitert werden können, ohne die 
 übrigen Funktionen zu beeinträchtigen. So können beispielsweise zum Start in der Library **Persistenz_UF** zunächst nur
 die Methoden zur Speicherung von Daten im Hauptspeicher enthalten sein, in einer späteren Version dann auch die 
 Methoden zur Datenspeicherung in Dateien oder Datenbanken.
 
 ## Library Config_UF
 Diese Library enthält alle Klassen und Methoden, um Config-Daten zu laden, zu verteilen und zu implementieren.
 
 ## Library API_UF
 Diese Library enthält alle Klassen und Methoden zur Erzeugung einer REST Api und zum Datentransfer darüber.
 
 ## Library Persistenz_UF
 Diese Library enthät alle Klassen und Methoden, um Daten in verschiedenen Speichern abzulegen bzw. daraus abzurufen.
 

# Datenströme/Datentypen

## Datenströme in Richtung Persistenz

Der auslösende Microservice (im Beispiel *hellos*) nimmt die Daten vom Nutzer entgegen. Für diese Daten werden in der
Regel die Grund-Datentypen – zum Beispiel **String, Integer oder Dictionary** – verwendet. Für die Erzeugung des 
Requests werden Methoden aus der Bibliothek *API_UF* zum Senden genutzt. Innerhalb dieser Methoden erfolgt ein encoding 
der aufgenommenen Nutzerdaten: in einem ersten Schritt von der Daten-Grundtypen in einen **JSON-String**, in einem 
zweiten Schritt in Daten vom Typ **Bytes**, damit diese an den empfangenen Microservice (im Beispiel *prints*) geschickt
werden können.

Der empfangene Microservice nimmt die Daten vom Typ **Bytes** auf und decodiert sie. Zunächst vom Typ **Bytes** in einen
**JSON-String**, im zweiten Schritt wieder zurück in die Grund-Datentypen. Um den Request innerhalb der Persistenz 
umzusetzen, werden Methoden aus der Bibliothek *CRUD_UF* genutzt. Diese übersetzen den jeweiligen Request in 
CRUD-Methoden (Create, Read, Update, Delete), um auf die Persistenz zuzugreifen. Dabei werden die Daten in Form der 
Grund-Datentypen übergeben. Die Persistenz wird in Form des Datentpys **Baum** verwaltet. Um die Speicherobjekte zu 
verändern, werden Methoden der Bibliothek *Persistenz_UF* verwendet. Diese schreiben oder lesen die Daten in oder aus
den Speicherobjekten. Auch dabei werden die Daten in Form der Grund-Datentypen übergeben. 

![Grafische Darstellung Programmarchitektur](https://github.com/StefSchneider/Unternehmensfaehigkeiten/blob/master/Dokumentation/Grafik_Programmarchitektur.png)

## Datenströme aus Richtung Persistenz



JSON wird nur im Aueßnverhältnis zwischen hellos und prints genutzt