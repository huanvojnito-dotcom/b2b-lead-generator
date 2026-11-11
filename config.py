import os
from dotenv import load_dotenv
from config import LOCATIONS, PROJECTS
from scraper import search_places, scrape_email_from_website, save_to_excel

# Betöltjük az .env fájlból az API kulcsot
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def main():
    if not GOOGLE_API_KEY:
        print("[Hiba] Nem található a GOOGLE_API_KEY az .env fájlban!")
        return

    print("=== B2B Lead Generátor ===")
    print("Válassz projektet:")
    for key, proj in PROJECTS.items():
        print(f"[{key}] {proj['name']}")

    choice = input("\nAdd meg a projekt számát: ")
    if choice not in PROJECTS:
        print("Érvénytelen választás.")
        return

    selected_project = PROJECTS[choice]
    categories = selected_project["categories"]
    output_file = selected_project["output_file"]
    unique_places = {}

    print(f"\nIndul a keresés: {selected_project['name']}...")

    # Google Maps kaparás
    for cat_query, cat_label in categories.items():
        for city in LOCATIONS:
            query = f"{cat_query} en {city}, España"
            print(f"Keresés: {query}")
            places = search_places(query, GOOGLE_API_KEY)

            for p in places:
                place_id = p.get("id")
                if not place_id or place_id in unique_places or p.get("businessStatus") != "OPERATIONAL":
                    continue
                unique_places[place_id] = {
                    "Kategória": cat_label,
                    "Keresett Város": city,
                    "Név": p.get("displayName", {}).get("text", ""),
                    "Telefonszám": p.get("nationalPhoneNumber", ""),
                    "Email": "",
                    "Weboldal": p.get("websiteUri", ""),
                    "Cím": p.get("formattedAddress", ""),
                    "Értékelés": p.get("rating", ""),
                    "Vélemények száma": p.get("userRatingCount", 0)
                }

    places_list = list(unique_places.values())
    if not places_list:
        print("Nincs találat.")
        return

    # Email keresés
    print(f"\n{len(places_list)} cég találva. Email keresés indul...")
    for idx, item in enumerate(places_list, 1):
        website = item["Weboldal"]
        if website:
            item["Email"] = scrape_email_from_website(website)
            if item["Email"]:
                print(f"[{idx}/{len(places_list)}] Találat: {item['Email']}")

    # Mentés
    save_to_excel(places_list, output_file)
    print(f"\nKész! {len(places_list)} lead mentve: {output_file}")


if __name__ == "__main__":
    main()