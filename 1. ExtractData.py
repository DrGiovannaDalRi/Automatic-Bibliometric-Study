###AUTOMATIC EXTRACTION OF DATA RELATED TO ARTICLES AND AUTHORS FOR A BIBLIOMETRIC STUDY
"""
Pipeline:

1. Retrieval of PMIDs associated with specific queries and periods via NCBI API
2. Filtering by Journal Impact Factor (IF)
3. Filtering according to type of article (comments, letters, reviews, etc)
4. Retrieval of immediate data:
    - Names and surnames of authors
    - Authorships
    - Journal of publication
    - Year of publication
5. Retrieval of gender of authors, through gender_guesser library
6. Retrieval of nationality of affiliation of authors via OpenAlex API (through PMIDs)
"""

##IMPORT LIBRARIES
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import gender_guesser.detector as gender

#API KEYS
EMAIL = "---"
API_KEY = "---"

#QUERY FOR PUBMED DATABASE SEARCH
QUERY = (
    '("Neurosurgical Procedures"[MeSH Terms] OR "Neurosurgery"[MeSH Terms] '
    'OR neurosurg*[Title/Abstract] OR neurosurgeon*[Title/Abstract] '
    'OR "Neurological Surgery"[Title/Abstract]) '
    'AND english[lang] '
    'NOT (Comment[pt] OR Editorial[pt] OR Letter[pt] OR News[pt] OR Published Erratum[pt] OR Retracted Publication[pt])'
)

#DEFINITION OF STUDY PERIOD
MINDATE = "2006/07/01"
MAXDATE = "2008/06/30"

#DEFINITION OF NAME VARIABLES
NAME = "SpinalNeurosurgery0608.xlsx"
NAMESTATS = "StatisticalAnalysis0608.xlsx"

#DEFINITION OF NCBI VARIABLES
RETMAX = 10000


## GENDER DETECTOR
detector = gender.Detector(case_sensitive=False)

def extract_firstname(fullname):
    """Extract first token from ForeName (handles middle names)."""
    if not fullname:
        return ""
    return fullname.split()[0]

def classify_gender(firstname):
    """Return male/female/X based on first name."""
    g = detector.get_gender(firstname)
    if g in ["female", "mostly_female"]:
        return "female"
    elif g in ["male", "mostly_male"]:
        return "male"
    else:
        return "X"   # Unknown → X


## SEARCH PMIDs
#The file JCRWantedJournals contains the journals with IF>=2, updated to 2026
def load_wanted_journals(path="JCRWantedJournals.xlsx"):
    df = pd.read_excel(path)
    wanted = set(df["Journal"].str.strip().str.lower())
    return wanted

def search_pmids(query, mindate, maxdate):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "mindate": mindate,
        "maxdate": maxdate,
        "datetype": "pdat",
        "retmax": RETMAX,
        "api_key": API_KEY,
        "email": EMAIL
    }
    r = requests.get(url, params=params)
    root = ET.fromstring(r.text)
    return [id_tag.text for id_tag in root.findall(".//Id")]

# SEARCH COUNTRY AFFILIATION VIA OPENALEX
def get_openalex_country(pmid):
    url = f"https://api.openalex.org/works/pmid:{pmid}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return ""

    data = r.json()
    authorships = data.get("authorships", [])
    if not authorships:
        return "",""

    first_inst = authorships[0].get("institutions", [])
    last_inst = authorships[-1].get("institutions", [])

    nat_first = first_inst[0].get("country_code", "") if first_inst else ""
    nat_last = last_inst[0].get("country_code", "") if last_inst else ""

    return nat_first, nat_last

# FETCH METADATA
def fetch_and_extract(pmids, wanted_journals, batch_size=100):
    results = []

    total = len(pmids)
    processed_count = 0
    removed_journal_count = 0
    kept_count = 0

    for i in range(0, len(pmids), batch_size):
        batch = pmids[i:i+batch_size]

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "rettype": "xml",
            "retmode": "xml",
            "api_key": API_KEY,
            "email": EMAIL
        }

        r = requests.get(url, params=params)
        text = r.text.strip()

        if not text:
            print(f"Empty response for batch {i//batch_size}")
            continue

        if text.startswith("<?xml"):
            text = text.split("?>", 1)[1].strip()

        try:
            root = ET.fromstring(text)
        except Exception as e:
            print(f"XML parse error in batch {i//batch_size}: {e}")
            continue

        for article in root.findall(".//PubmedArticle"):
            processed_count += 1
            print(f"Analyzed {processed_count} / {total}")

            try:
                pmid = article.find(".//PMID").text

                # Journal
                journal = article.find(".//Journal/Title").text.strip()
                journal_norm = journal.lower()

                if journal_norm not in wanted_journals:
                    removed_journal_count += 1
                    continue

                # Authors
                authors = article.findall(".//Author")
                first = authors[0]
                last = authors[-1]

                first_name_full = f"{first.findtext('ForeName', '')} {first.findtext('LastName', '')}".strip()
                last_name_full  = f"{last.findtext('ForeName', '')} {last.findtext('LastName', '')}".strip()

                # Extract first names
                first_firstname = extract_firstname(first.findtext("ForeName", ""))
                last_firstname  = extract_firstname(last.findtext("ForeName", ""))

                # Gender classification via gender_guesser
                first_gender = classify_gender(first_firstname)
                last_gender  = classify_gender(last_firstname)

                # Publication date
                pubdate = article.find(".//JournalIssue/PubDate")
                year = pubdate.findtext("Year", "")
                month = pubdate.findtext("Month", "")
                day = pubdate.findtext("Day", "")
                date = f"{year}-{month}-{day}".strip("-")

                # Nationality via OpenAlex
                nat_first, nat_last = get_openalex_country(pmid)

                results.append({
                    "PMID": pmid,
                    "FirstAuthor": first_name_full,
                    "LastAuthor": last_name_full,
                    "FirstNationality": nat_first,
                    "LastNationality": nat_last,
                    "PublicationDate": date,
                    "Journal": journal,

                    # Gender columns
                    "FirstAuthor_Female": "1" if first_gender == "female" else ("X" if first_gender == "X" else "0"),
                    "FirstAuthor_Male": "1" if first_gender == "male" else ("X" if first_gender == "X" else "0"),
                    "LastAuthor_Female": "1" if last_gender == "female" else ("X" if last_gender == "X" else "0"),
                    "LastAuthor_Male": "1" if last_gender == "male" else ("X" if last_gender == "X" else "0"),

                })

                kept_count += 1

            except Exception:
                continue

    return results, processed_count, removed_journal_count, kept_count

## MAIN
def main():
    pmids = search_pmids(QUERY, MINDATE, MAXDATE)
    original_count = len(pmids)
    print(f"Found {original_count} PMIDs")

    wanted_journals = load_wanted_journals("JCRWantedJournals.xlsx")

    data, processed_count, removed_journal_count, kept_count = fetch_and_extract(pmids, wanted_journals)

    df = pd.DataFrame(data)
    df.to_excel(NAME, index=False)

    stats = pd.DataFrame({
        "Metric": [
            "Analysed reports",
            "Removed (journal IF)",
            "Reports kept"
        ],
        "Value": [
            processed_count,
            removed_journal_count,
            kept_count
        ]
    })

    stats.to_excel(NAMESTATS, index=False)

if __name__ == "__main__":
    main()
