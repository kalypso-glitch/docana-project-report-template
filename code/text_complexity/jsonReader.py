# uses json to read newline-delimited JSON files in a memory efficient way
import json
import csv

def read_json_file(file_path: str, csv_function: callable, destination_file: str, iterations: int = None):
    """
    Read a newline-delimited JSON file and apply a csv function to each item, saving results to a CSV file.
    The header field names are taken from the first mapped item.
    
    Args:
        file_path: Path to the source JSON file
        csv_function: Function to apply to each item, result written to destination CSV file. Must return a dictionary.
        destination_file: Path where mapped results will be saved as CSV
        iterations: Maximum number of JSON objects to process. If None, process all objects.
    """
    if iterations is not None and iterations <= 0:
        return 0

    item_count = 0
    csv_writer = None
    field_names = None

    with open(file_path, 'r', encoding='utf-8') as f, open(destination_file, 'w', newline='', encoding='utf-8') as csv_file:
        for line in f:
            line = line.strip()
            if not line:
                continue

            item = json.loads(line)
            mapped_item = csv_function(item)
            if not isinstance(mapped_item, dict):
                raise ValueError("Mapping function must return a dictionary")

            if csv_writer is None:
                field_names = list(mapped_item.keys())
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
                csv_writer.writeheader()

            csv_writer.writerow(mapped_item)
            item_count += 1

            if item_count % 10000 == 0:
                print(f"Processed {item_count} items...")

            if iterations is not None and item_count >= iterations:
                break

    return item_count
        