import pandas as pd
from scraper.config import EXCEL_FILE_PATH, EXCEL_SHEET_NAME, ID_LIST_PATH

def extract_ids():
    """Extract property IDs from Excel file and save to text file."""
    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=EXCEL_SHEET_NAME)

        # Validate that 'QuickRef' column exists
        if 'QuickRef' not in df.columns:
            raise ValueError("The Excel file must contain a 'QuickRef' column.")

        # Filter rows where 'QuickRef' starts with 'R' and directly convert to a list
        ids = df[df['QuickRef'].str.startswith('R', na=False)]['QuickRef'].tolist()

        # Check if the list is empty, and provide helpful output
        if not ids:
            print("No IDs found starting with 'R'.")
            return 0
        else:
            # Write the IDs to the output file
            with open(ID_LIST_PATH, 'w') as f:
                for id_val in ids:
                    f.write(f"{id_val}\n")
            print(f"Successfully extracted {len(ids)} IDs starting with 'R' and saved them to {ID_LIST_PATH}")
            return len(ids)

    except FileNotFoundError:
        print(f"Error: The file '{EXCEL_FILE_PATH}' was not found.")
        return 0
    except pd.errors.SheetNameNotFound:
        print(f"Error: The sheet '{EXCEL_SHEET_NAME}' was not found in the Excel file.")
        return 0
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

if __name__ == "__main__":
    extract_ids()