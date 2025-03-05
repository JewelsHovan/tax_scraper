# Tax Data Scraper

A high-performance web scraper for collecting property tax data from tax assessment websites. This project implements an asynchronous scraping system with checkpointing capabilities to efficiently gather tax information for multiple properties.

## Project Overview

This tool automates the process of collecting property tax information by:
1. Extracting property IDs from Excel files
2. Making concurrent HTTP requests to tax assessment websites
3. Parsing responses to extract tax amounts
4. Saving and processing the results

## Features

- **Asynchronous Processing**: Implements concurrent requests (5 simultaneous requests) for improved performance
- **Checkpointing**: Automatically saves progress every 10,000 requests to prevent data loss
- **Rate Limiting**: Configured for optimal performance (1,000 requests per minute per worker, 10 workers total)
- **Error Handling**: Robust error handling for failed requests and invalid responses
- **Data Processing**: Structured output with detailed tax information
- **Progress Tracking**: Real-time progress monitoring and statistics

## Project Structure

```
tax_scraper/
├── data/                 # Directory for input/output data
├── scraper/             # Core scraping module
│   ├── config.py        # Configuration settings
│   ├── extract_ids.py   # Property ID extraction logic
│   ├── scrape_ids.py    # Main scraping implementation
│   └── process_data.py  # Data processing and analysis
├── run.py               # Main orchestration script
└── README.md           # Project documentation
```

## Setup and Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure settings in `scraper/config.py`

## Usage

1. Place your input Excel file with property IDs in the `data` directory
2. Run the main script:
   ```bash
   python run.py
   ```

## Process Flow

1. **Data Preparation**
   - Reads property IDs from the input Excel file
   - Validates and formats IDs
   - Creates a text file with processed IDs

2. **Scraping Process**
   - Initializes async worker pool (10 workers)
   - Each worker handles 1,000 requests per minute
   - Makes HTTP requests to tax website
   - Parses HTML responses using BeautifulSoup
   - Extracts total amount due from specific table cells

3. **Data Processing**
   - Processes raw scraped data
   - Calculates statistics and summaries
   - Generates structured output files

4. **Checkpointing**
   - Saves progress every 10,000 requests
   - Maintains recovery points in case of interruption

## Performance

- Total Capacity: 10,000 requests per minute
- Workers: 10 concurrent workers
- Requests per Worker: 1,000 rpm
- Checkpoint Frequency: Every 10,000 requests

## Output

The script generates:
- Processed tax data in structured format
- Summary statistics including:
  - Total properties processed
  - Properties with payments
  - Properties with outstanding balances
  - Average outstanding balance
  - Processing time statistics

## Error Handling

- Graceful handling of network failures
- Retry mechanism for failed requests
- Logging of unprocessable properties
- Data validation at each step

## Future Improvements

- [ ] Implement more sophisticated rate limiting
- [ ] Add support for multiple tax assessment websites
- [ ] Enhance error reporting and logging
- [ ] Implement data validation checks
- [ ] Add support for different input file formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
