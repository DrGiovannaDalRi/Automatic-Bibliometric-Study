# Automatic-Bibliometric-Study

## Author
Dr. Giovanna Dal Rì, Medical Doctor and Biomedical Engineer

## Motivation
The scripts were implemented for an automatic bibliometric study submitted to a scientific journal.

## Description
The code for extraction automatically retrieves the data of the articles in specific fields throughout specific periods. The extracted data are country of affiliation, authorship, journal and year of publication, and gender of the authors. 

The code for statistics analyses the obtained results, aiming at quantifying the gender gap that is still present in the neurosurgery field.

## Pipeline
Extraction:
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
The gender of the authors was retrieved via the gender_guesser library, which inferes gender from names. 
The country of affiliation of the authors was obtained via the OpenAlex API, using the PMIDs of the articles.

Only the papers published on a journal with IF>=2 are kept, to investigate only high-impact journals. Moreover, non peer-reviewed scientific articles, such as comments or letters to the editor, were removed.

Unfortunately, countries like China and Taiwan do not allow gender inference from names, due to reasons deeply-rooted in their culture. Accordingly, authors having affiliations in China and Taiwan were removed from the dataset, reducing significantly the risk of misgender and bias. 

A PRISMA pipeline was followed throughout.

### Statistics
The number and percentage of women as general, first and last authors were computed. Moreover, Chi-Squared Tests of Independence comparing the observed distribution of women and men authors against a 50/50 distribution were conducted. A p-value < 0.05 was considered statistically significant. Gendered authorship combinations were analysed, to discover the distributions of women and men in junior and senior roles. 

The percentages of women authors were computed across the study period. In addition, a Chi-Squared test was performed for each year, comparing the observed proportions of women and men in first and last authorship against an expected 50/50 distribution. 

Yearly trends of women as first and last authors throughout the study period were studied, producing a time plot. Moreover, the different growth between first and last authors was analysed, aiming at producing a Gender Representation Gap (GRG) curve.

The percentage of women as first and last authors was also analysed per each country of affiliation, discovering which countries had the highest percentage of women first and last authors and which, on the other hand, had the highest gender gap. 
Moreover, yearly trends of women as first and last authors were also computed per each country, in order to analyse the growth of women authors in each nation, especially the best and the worst ones.

Finally, the percentage of women as first and last authors was studied per each journal of publication.
   
In order to maintain statistical significance, a threshold was applied to both the number of articles published on specific journals and countries. In this way, the low-output journals and countries would not compromise the statistics.

## Results
The  following histogram shows the gendered authorships combinations:

<div align="center">
<img width="475" height="301" alt="Figure2" src="https://github.com/user-attachments/assets/0cd17e0e-5fb9-4d91-94f6-2748879ab1d0" />
</div>

The yearly trend for two of the countries is shown in the following plot:

<div align="center">
<img width="525" height="540" alt="Figure6" src="https://github.com/user-attachments/assets/f6771829-da47-4e08-9c2b-910227dab66a" />
</div>

The percentages of women first and last authors per journal of publication are shown in the following barplot:

<div align="center">
<img width="525" height="575" alt="Figure7" src="https://github.com/user-attachments/assets/31c60871-49ef-4ea4-baa1-8ba8835a4609" />
</div>

For complete results, please refer to the forthcoming manuscript.

## Limitations
A notable limitation is gender inference based on names, which may introduce classification errors. Moreover, only binary gender categories were considered, as non-binary identities cannot be determined solely from names, introducing a potential bias in gender classification.

Removing China and Taiwan from the study represents another notable limitation, but it was necessary to decrease the risk of misgendering, which would otherwise have been high.

All the used thresholds, in both countries and journals, may limit the visibility of some countries or journals. However, they were implemented to improve the quality of the research and reduce the introduction of biases due to low output frequencies.

Although PubMed remains the most comprehensive biomedical database, reliance on a single source may introduce structural biases in the composition of the dataset. 

## Tech Stack
* Language: Python 3.10+
* Libraries: see requirements.txt
* OpenAlex API Key
* NCBI API Key

## Materials
* JCRWantedJournals.xlsx contains all the journals with IF>=2, which is proprietary data and cannot be published on GitHub

## License
This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

Under this license, you are free to use, modify, and distribute the code for academic or commercial purposes, provided that original authorship is attributed and modified files retain notices of changes.

## Citation
If you use this code, the extraction pipeline, or the statistical analysis in your research, please cite it as follows:

> Dal Rì, 2026. *Automatic Bibliometric Study* (Version 1.0.0) [Computer software]. GitHub. https://github.com/DrGiovannaDalRi/Automatic-Bibliometric-Study

**BibTeX:**
```bibtex
@software{DalRi2026,
  author = {Dal Rì, Giovanna},
  title = {Automatic Bibliometric Study},
  year = {2026},
  version = {v1.0.0},
  url = {[(https://github.com/DrGiovannaDalRi/Automatic-Bibliometric-Study)]
}
