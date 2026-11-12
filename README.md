# B2B Lead Generator

A Python command-line tool that builds B2B prospect lists for local businesses in the Valencia region (Spain). It searches Google Maps through the **Google Places API (New)**, visits each business website to find a public contact email, and exports the results to an Excel file ready for sales outreach.

I built it to find potential clients for an AI-automation service aimed at small businesses (clinics, travel agencies, car-parts shops).

## Features

- **Ready-made search profiles** – travel agencies, clinics (dental, podiatry, veterinary) and car parts / scrapyards, each with several search terms
- **Wide coverage** – searches 39 towns within roughly 100 km of Valencia, from Castellón to Benidorm
- **Pagination** – follows `nextPageToken` to collect every result page, not only the first 20 places
- **Clean data** – removes duplicates by place ID and keeps only businesses that are currently operational
- **Email discovery** – scans the homepage and, if nothing is found, common subpages (`/contacto`, `/contact`, `/aviso-legal`, `/politica-de-privacidad`); handles obfuscated addresses such as `name[at]domain.com` and filters out false positives (image files, tracking domains, placeholder addresses)
- **Excel export** – sorted by category, town and number of reviews, so the most established businesses appear first

## How it works

```
Choose a project → Places API text search (category × town)
    → de-duplicate & keep OPERATIONAL businesses
    → scrape each website for an email address
    → export to .xlsx
```

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point: project menu, search loop, de-duplication and progress output |
| `config.py` | Target towns (`LOCATIONS`) and search profiles (`PROJECTS`) |
| `scraper.py` | Places API client, website email scraper and Excel export |
| `requirements.txt` | Python dependencies |

## Requirements

- Python 3.10 or newer
- A Google Cloud API key with the **Places API (New)** enabled (billing must be active in Google Cloud)

## Installation

```bash
git clone https://github.com/huanvojnito-dotcom/b2b-lead-generator.git
cd b2b-lead-generator
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```
GOOGLE_API_KEY=your_api_key_here
```

The `.env` file is listed in `.gitignore`, so the key is never committed.

## Usage

```bash
python main.py
```

Choose a project number from the menu (for example `2` for clinics). The tool prints its progress and saves the results to the file defined for that project, e.g. `klinikak_100km.xlsx`.

### Output columns

The program's console messages and column headers are currently in Hungarian:

| Column | Meaning |
|--------|---------|
| Kategória | Category |
| Keresett Város | Town searched |
| Név | Business name |
| Telefonszám | Phone number |
| Email | Email address(es) found, up to 3 |
| Weboldal | Website |
| Cím | Address |
| Értékelés | Google rating |
| Vélemények száma | Number of reviews |

## Customisation

Edit `config.py`:

- Add or remove towns in `LOCATIONS`
- Add a new search profile to `PROJECTS` with a name, an output file and a set of search terms

## Responsible use

- Respect the [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms), including the limits on storing Places data.
- Collected contact data is subject to the GDPR and, in Spain, to the LSSI rules on commercial email. Use the leads for a personal, relevant first contact rather than bulk unsolicited mailing.
- Each run makes many Places API requests, which can generate costs. Check your Google Cloud quotas before large searches.

## Possible improvements

- Command-line arguments instead of the interactive menu
- English labels and output columns
- Parallel website scraping to speed up email discovery
- Re-enable SSL certificate verification with a fallback only for sites that fail
- Unit tests for the email-extraction logic

## Development note

This project was developed with the help of an AI coding assistant (Claude). I designed the workflow, reviewed and tested the code, and iterated on fixes until it worked reliably on real data.
