"""
This module provides functionality to asynchronously scrape property tax information
from a tax search website.
"""

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time
import csv
from scraper.config import (
    BASE_URL, HEADERS, BATCH_SIZE, NUM_WORKERS,
    CHECKPOINT_SIZE, ID_LIST_PATH, TAX_RESULTS_PATH
)

async def scrape_id_async(id, session):
    """
    Asynchronously scrapes property tax information for a given ID.
    """
    try:
        async with session.get(BASE_URL.format(id=id), headers=HEADERS) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            amount_element = soup.find("td", id="dnn_ctr368_View_tdPMTotalDue")
            total_due_amount = amount_element.text.strip() if amount_element else "Could not find total due"

            payment_history_table = soup.find("table", {"id": "tblPaymentHistoryData"})
            payment_history = []

            if payment_history_table:
                data_rows = payment_history_table.find_all("tr")[1:]
                for row in data_rows:
                    cells = row.find_all("td")
                    if cells:
                        tax_year = cells[0].text.strip()
                        transaction_date = cells[1].text.strip()
                        effective_date = cells[2].text.strip()
                        payment_amount = cells[3].text.strip()
                        receipt_link = cells[4].find("a")
                        receipt_number = receipt_link.text.strip() if receipt_link else cells[4].text.strip()
                        payment_history.append([tax_year, transaction_date, effective_date, payment_amount, receipt_number])
            else:
                payment_history = "Could not find payment history table"

            return id, {
                'total_due': total_due_amount,
                'payment_history': payment_history
            }

    except Exception as e:
        return id, f"Error scraping ID {id}: {str(e)}"

async def save_checkpoint(data, is_first_write):
    """Save results to CSV file."""
    mode = 'w' if is_first_write else 'a'
    with open(TAX_RESULTS_PATH, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        if is_first_write:
            writer.writerow(['Property ID', 'Result'])
        for id, result in data:
            writer.writerow([id, result])
    print(f"Checkpoint saved: {len(data)} results written to {TAX_RESULTS_PATH}")

async def worker(worker_id, ids_chunk, processed_count, checkpoint_size):
    """Worker process to handle a chunk of IDs."""
    worker_results = []
    for i in range(0, len(ids_chunk), BATCH_SIZE):
        batch = ids_chunk[i:i+BATCH_SIZE]
        async with aiohttp.ClientSession() as session:
            tasks = [scrape_id_async(id, session) for id in batch]
            batch_results = await asyncio.gather(*tasks)
            worker_results.extend(batch_results)

            processed_count.value += len(batch)
            if processed_count.value % checkpoint_size == 0:
                await save_checkpoint(worker_results, processed_count.value == checkpoint_size)
                worker_results = []

            print(f"Worker {worker_id}: Processed {len(batch)} IDs (Total: {processed_count.value})")
    return worker_results

async def scrape_all_ids(ids_list):
    """
    Main function to scrape all property IDs.
    Returns the total number of processed IDs.
    """
    class Counter:
        def __init__(self):
            self.value = 0
    processed_count = Counter()

    chunk_size = len(ids_list) // NUM_WORKERS
    if len(ids_list) % NUM_WORKERS > 0:
        chunk_size += 1

    id_chunks = [ids_list[i:i+chunk_size] for i in range(0, len(ids_list), chunk_size)]
    worker_tasks = [
        worker(i, chunk, processed_count, CHECKPOINT_SIZE)
        for i, chunk in enumerate(id_chunks)
    ]
    
    final_results = await asyncio.gather(*worker_tasks)

    # Save any remaining results
    remaining_results = []
    for chunk_result in final_results:
        remaining_results.extend(chunk_result)

    if remaining_results:
        await save_checkpoint(remaining_results, processed_count.value < CHECKPOINT_SIZE)

    return processed_count.value

def run_scraper():
    """
    Main entry point for the scraper.
    Returns the number of processed IDs.
    """
    try:
        with open(ID_LIST_PATH, 'r') as f:
            ids_list = f.read().splitlines()
        
        print(f"\n--- Scraping Property Tax Information ---")
        print(f"Using {NUM_WORKERS} workers with batch size of {BATCH_SIZE}")
        
        start_time = time.time()
        total_processed = asyncio.run(scrape_all_ids(ids_list))
        total_time = time.time() - start_time
        
        print(f"\nTotal scraping time: {total_time:.2f} seconds")
        print(f"Average time per ID: {(total_time/len(ids_list)):.2f} seconds")
        print(f"Results have been written to {TAX_RESULTS_PATH}")
        
        return total_processed
        
    except FileNotFoundError:
        print(f"Error: ID list file not found at {ID_LIST_PATH}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

if __name__ == "__main__":
    run_scraper()
