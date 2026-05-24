import csv
import os


class CSVReader:
    @staticmethod
    def read_csv(file_name):
        data = []
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "data", file_name)
        with open("data/price_range.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cleaned_row = {
                    key.strip(): value.strip()
                    for key, value in row.items()
                }
                data.append(cleaned_row)
        return data