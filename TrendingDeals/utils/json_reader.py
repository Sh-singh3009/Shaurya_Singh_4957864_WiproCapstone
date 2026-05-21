import json

class JsonReader:
    @staticmethod
    def read_categories(file_path):
        with open("data/categories.json", "r") as file:
            data = json.load(file)
        return data["categories"]