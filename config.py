LOCATIONS = [
    "Valencia", "Torrent", "Paterna", "Mislata", "Burjassot", "Catarroja", "Paiporta", "Aldaia",
    "Sagunto", "Puerto de Sagunto", "Llíria", "Bétera", "Ribarroja del Turia",
    "Alzira", "Cullera", "Sueca", "Carcaixent", "Algemesí",
    "Gandía", "Oliva", "Tavernes de la Valldigna",
    "Xàtiva", "Ontinyent", "Alcoy", "Ibi",
    "Requena", "Utiel", "Chiva", "Buñol",
    "Castellón de la Plana", "Villarreal", "Burriana", "Vall de Uxó", "Vinaròs", "Segorbe",
    "Dénia", "Jávea", "Calpe", "Benidorm"
]

# Itt definiáljuk a különböző kaparási profilokat
PROJECTS = {
    "1": {
        "name": "Agencias de Viajes (Utazási irodák)",
        "output_file": "agencias_viajes_100km.xlsx",
        "categories": {
            "agencia de viajes": "Agencia de Viajes",
            "mayorista de viajes": "Mayorista de Viajes",
            "agencia de viajes minorista": "Agencia Minorista"
        }
    },
    "2": {
        "name": "Clínicas (Klinikák)",
        "output_file": "klinikak_100km.xlsx",
        "categories": {
            "clínica dental": "Fogászat (Dental)",
            "clínica podológica": "Podológia (Podología)",
            "clínica veterinaria": "Állatorvos (Veterinaria)"
        }
    },
    "3": {
        "name": "Recambios y Desguaces (Autóalkatrész és bontó)",
        "output_file": "autoalkatreszek_100km.xlsx",
        "categories": {
            "recambios de coche": "Autóalkatrész bolt",
            "desguace": "Autóbontó",
            "recambios y accesorios para coches": "Alkatrész és tartozék"
        }
    }
}