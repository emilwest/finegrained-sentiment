[Westin, E. (2020). Fine-grained sentiment analysis of product reviews in Swedish.](https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1492746&dswid=3932)

Bibtex:
@misc{westin2020fine,
  title={Fine-grained sentiment analysis of product reviews in Swedish},
  author={Westin, Emil},
  year={2020}
}

# finegrained-sentiment
New repository with cleaned up files for bachelor thesis in language technology 

# List of all files and folders:

## Folders
- csv_from_webscraper : contains one csv per category retrieved from webscraper.py 


## Python
- webscraper.py : used for downloading data sets from prisjakt.se

## CSV
- total_reviews.csv : contains all reviews 

## R
- analysis.R : create total_reviews.csv from all individual csv files by category, removing reviews with no content (only ratings)

