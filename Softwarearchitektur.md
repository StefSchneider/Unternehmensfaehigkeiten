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