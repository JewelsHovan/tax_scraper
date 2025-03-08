# paths
DATA_PATH = "/Users/julienh/Desktop/ScrapingProjects/tax_scraper/data"
EXCEL_FILE_PATH = f"{DATA_PATH}/ALLQuickRefNumbers.xlsx"
EXCEL_SHEET_NAME = "2025-01-17_006376_APPRAISAL_INF"
ID_LIST_PATH = f"{DATA_PATH}/id_list.txt"
TAX_RESULTS_PATH = f"{DATA_PATH}/tax_results.csv"

# Scraping configuration
BASE_URL = "http://taxsearch.co.grayson.tx.us:8443/Property-Detail/PropertyQuickRefID/{id}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}
BATCH_SIZE = 3  # Number of concurrent requests per worker
NUM_WORKERS = 5  # Number of worker sessions to use
CHECKPOINT_SIZE = 100  # Save results to CSV after this many records
DELAY = 0.5  # Delay between requests in seconds
MAX_RETRIES = 3
FAILED_IDS_PATH = "failed_ids.txt"