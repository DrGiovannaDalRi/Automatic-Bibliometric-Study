# Automatic-Bibliometric-Study

## Author
Dr. Giovanna Dal Rì, Medical Doctor and Biomedical Engineer

giovanna.dalri.doctor@proton.me

## Motivation
The codes were implemented for an automatic bibliometric study submitted to a scientific journal.

## Description
The code for extraction automatically retrieves the data of the articles in specific fields throughout specific periods. The extracted data are country of affiliation, authorship, journal and year of publication, and gender of the authors. 

The code for statistics analyses the obtained results, aiming at quantifying the gender gap that is still present in the neurosurgery field.

## Pipeline
Extraction:
1. Retrieval of PMIDs associated to specific queries and periods via NCBI API
2. Filtering according to IF of journals
3. Filtering according to type of article (comments, letters, reviews, etc)
4. Retrieval of immediate data:
  - Names and surnames of authors
  - Authorships
  - Journal of publication
  - Year of publication
5. Retrieval of gender of authors, through gender_guesser library
6. Retrieval of nationality of affiliation of authors via OpenAlex API (through PMIDs)

Statistics:
1. Number and percentage of women as first and last authors
2. Computation of Chi-Squared Values
3. Yearly trends of women as first and last authors throughout the study period
4. Percentage of women as first and last authors per each country of affiliation
5. Yearly trends of women as first and last authors per each country of affiliation
6. Percentage of women as first and last authors per each journal of publication

### Extraction
The code retrieves all the articles related to a specific query and time period via PubMed (NCBI). 
Specific data were then retrieved directly from PubMed via NCBI API, like PMIDs, the names and surnames of authors, their authorships, the journal of publication, and the year of publication.
The gender of the authors was retrieved via the gender_guesser library, which interferes gender from names. 
The country of affiliation of the authors was obtained via the OpenAlex API, using the PMIDs of the articles.

Only the papers published on a journal with IF>=2 are kept, to investigate only high-impact journals. Moreover, non peer-reviewed scientific articles, such as comments or letters to the editor, were removed.

Unfortunately, countries like China and Taiwan do not allow interference of gender from names, due to reasons deeply-rooted in their culture. Accordingly, authors having affiliations in China and Taiwan were removed from the dataset, reducing significantly the risk of misgender and bias. 

A PRISMA pipeline was followed throughoutly.

### Statistics
1. Number and percentage of women as first and last authors
2. Computation of Chi-Squared Values
3. Yearly trends of women as first and last authors throughout the study period
4. Percentage of women as first and last authors per each country of affiliation
5. Yearly trends of women as first and last authors per each country of affiliation
6. Percentage of women as first and last authors per each journal of publication
   
In order to maintain the statistical significance, a threshold was applied to both the number of articles published on certain journals and in certain countries. In this way, the low research outputs of certain journals and countries would not compromise the statistics.


## Results
The code was used to study the gender gap in neurosurgery across all countries and high-impact journals.

## Limitations
