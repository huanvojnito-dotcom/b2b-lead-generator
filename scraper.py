import requests
import pandas as pd
import time
import re
from urllib.parse import urljoin
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
IGNORE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js', '.woff', '.ttf', '.mp4', '.pdf')
IGNORE_DOMAINS = ('sentry.io', 'wixpress.com', 'example.com', 'domain.com', 'wordpress.org', 'w3.org', 'google.com', 'instagram.com', 'facebook.com')

def extract_emails_from_html(html_text):
    clean_text = html_text.replace('%40', '@').replace('&#64;', '@').replace('[at]', '@')
    found = re.findall(EMAIL_REGEX, clean_text)
    valid_emails = set()
    for email in found:
        email = email.lower().strip('.,;:"\'()[]<>')
        if not email.endswith(IGNORE_EXTENSIONS) and not any(d in email for d in IGNORE_DOMAINS):
            valid_emails.add(email)
    return list(valid_emails)

def scrape_email_from_website(url):
    if not url:
        return ""
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    all_emails = set()
    try:
        resp = requests.get(url, headers=headers, timeout=6, verify=False)
        if resp.status_code == 200:
            for e in extract_emails_from_html(resp.text):
                all_emails.add(e)
        if not all_emails:
            subpages = ['/contacto', '/contact', '/aviso-legal', '/politica-de-privacidad']
            for path in subpages:
                try:
                    sub_url = urljoin(url, path)
                    resp_sub = requests.get(sub_url, headers=headers, timeout=5, verify=False)
                    if resp_sub.status_code == 200:
                        found_sub = extract_emails_from_html(resp_sub.text)
                        if found_sub:
                            for e in found_sub:
                                all_emails.add(e)
                            break
                except Exception:
                    continue
        return ", ".join(list(all_emails)[:3])
    except Exception:
        return ""

def search_places(query_text, api_key):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.googleMapsUri,places.businessStatus,nextPageToken"
    }
    results = []
    page_token = None
    while True:
        payload = {"textQuery": query_text, "languageCode": "es", "regionCode": "ES", "pageSize": 20}
        if page_token:
            payload["pageToken"] = page_token
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code != 200:
                break
            data = response.json()
            results.extend(data.get("places", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
            time.sleep(2)
        except Exception:
            break
    return results

def save_to_excel(places_list, filename):
    df = pd.DataFrame(places_list)
    if not df.empty:
        df = df.sort_values(by=["Kategória", "Keresett Város", "Vélemények száma"], ascending=[True, True, False])
    df.to_excel(filename, index=False)