import ast
import numpy as np
import pandas as pd
from scraper.config import TAX_RESULTS_PATH

# Helper Functions
def _parse_result(result_str):
    """Safely parses a string representation of a dictionary."""
    try:
        return ast.literal_eval(result_str)
    except (ValueError, SyntaxError):
        return {'total_due': 'Error parsing', 'payment_history': []}

def _currency_to_float(currency_str):
    """Converts a currency string to a float, handling common issues."""
    if not isinstance(currency_str, str):
        return np.nan
    if 'Could not find total due' in currency_str or currency_str == 'N/A':
        return np.nan
    try:
        return float(currency_str.replace('$', '').replace(',', ''))
    except ValueError:
        return np.nan

def _safe_parse_date(date_str):
    """Parses a date string to datetime, handling errors."""
    if not isinstance(date_str, str):
        return pd.NaT
    try:
        return pd.to_datetime(date_str, format='%m-%d-%Y')
    except ValueError:
        return pd.NaT

def _payment_to_float(payment_str):
    """Converts a payment string to a float."""
    return _currency_to_float(payment_str) if isinstance(payment_str, str) else np.nan

def _get_latest_payment(payment_history):
    """Extracts the most recent payment from a payment history list."""
    if not payment_history or isinstance(payment_history, str):
        return {
            'Latest Tax Year': np.nan,
            'Transaction Date': pd.NaT,
            'Effective Date': pd.NaT,
            'Payment Amount': np.nan,
            'Receipt Number': np.nan
        }

    try:
        dated_entries = []
        for entry in payment_history:
            try:
                date_obj = pd.to_datetime(entry[1], format='%m-%d-%Y')
                dated_entries.append((date_obj, entry))
            except ValueError:
                continue

        if dated_entries:
            dated_entries.sort(reverse=True)
            latest = dated_entries[0][1]
            return {
                'Latest Tax Year': latest[0] if latest[0] else np.nan,
                'Transaction Date': _safe_parse_date(latest[1]),
                'Effective Date': _safe_parse_date(latest[2]),
                'Payment Amount': _payment_to_float(latest[3]),
                'Receipt Number': latest[4] if latest[4] else np.nan
            }
    except Exception as e:
        print(f"Error processing payment history: {e}")

    return {
        'Latest Tax Year': np.nan,
        'Transaction Date': pd.NaT,
        'Effective Date': pd.NaT,
        'Payment Amount': np.nan,
        'Receipt Number': np.nan
    }

def process_tax_data(input_file=TAX_RESULTS_PATH):
    """
    Processes tax data from a CSV file, extracting relevant information.
    Returns a structured DataFrame containing the processed data.
    """
    try:
        tax_results = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File not found at {input_file}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"Error: File at {input_file} is empty.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred reading {input_file}: {e}")
        return pd.DataFrame()

    processed_data = []
    for _, row in tax_results.iterrows():
        result_dict = _parse_result(row['Result'])
        total_due_float = _currency_to_float(result_dict.get('total_due', 'N/A'))
        latest_payment = _get_latest_payment(result_dict.get('payment_history', []))

        record = {
            'Property ID': row['Property ID'],
            'Total Due': total_due_float,
            **latest_payment
        }
        processed_data.append(record)

    return pd.DataFrame(processed_data)

def run_processor():
    """
    Main entry point for the data processor.
    Returns the processed DataFrame.
    """
    print("\n--- Processing Tax Data ---")
    df = process_tax_data()
    if not df.empty:
        print(f"Successfully processed {len(df)} records")
    return df

if __name__ == "__main__":
    run_processor()