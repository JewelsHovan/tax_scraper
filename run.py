"""
Main orchestration script for the tax scraping process.
This script coordinates the extraction of IDs, scraping of tax data,
and processing of results.
"""

import os
import time
from scraper.extract_ids import extract_ids
from scraper.scrape_ids import run_scraper
from scraper.process_data import run_processor
from scraper.config import DATA_PATH

def ensure_data_directory():
    """Ensure the data directory exists."""
    os.makedirs(DATA_PATH, exist_ok=True)

def main():
    """Main orchestration function."""
    start_time = time.time()
    
    print("=== Starting Tax Data Collection Process ===\n")
    
    # Ensure data directory exists
    ensure_data_directory()
    
    # Step 1: Extract IDs from Excel
    print("Step 1: Extracting property IDs from Excel...")
    num_ids = extract_ids()
    if num_ids == 0:
        print("Failed to extract IDs. Stopping process.")
        return
    print(f"Successfully extracted {num_ids} IDs.\n")
    
    # Step 2: Scrape tax data for each ID
    print("Step 2: Scraping tax data...")
    num_scraped = run_scraper()
    if num_scraped == 0:
        print("Failed to scrape tax data. Stopping process.")
        return
    print(f"Successfully scraped {num_scraped} properties.\n")
    
    # Step 3: Process and structure the results
    print("Step 3: Processing results...")
    results_df = run_processor()
    if results_df.empty:
        print("Failed to process results.")
        return
    
    # Calculate and display summary statistics
    total_time = time.time() - start_time
    print("\n=== Process Complete ===")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Total properties processed: {len(results_df)}")
    print(f"Average time per property: {total_time/len(results_df):.2f} seconds")
    
    # Display basic statistics about the results
    print("\nResults Summary:")
    print(f"Total properties with payments: {results_df['Payment Amount'].notna().sum()}")
    print(f"Total properties with outstanding balance: {results_df['Total Due'].notna().sum()}")
    print(f"Average outstanding balance: ${results_df['Total Due'].mean():.2f}")

if __name__ == "__main__":
    main()