"""
Der Microservice fragt per GET den aktuellen Stand des Microservice prints ab und druckt diesen aus
"""

import API_UF

if __name__ == "__main__":
    while True:
        nummer_ressource: int = input("Auf welche Ressource möchten Sie zugreifen (Nr.)? ")
        last_prints_API = API_UF.API()
        last_prints_API.url_partner = "http://localhost:31002/prints/" + str(nummer_ressource)
        uebergabedaten_ein = last_prints_API.hole({})
        print("Aktueller Text: ", uebergabedaten_ein["1"]["daten"])