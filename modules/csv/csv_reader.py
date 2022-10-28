from csv import DictReader
from typing import Iterable, Text

def parse_csv(csv_file: Iterable[Text])->list:
    csv_reader = DictReader(f=csv_file)
    table = []

    for row in csv_reader:
        table.append(row)
    return table

def read_csv(file_path: str)->list:

    csv_file = open(file_path,'r', encoding="utf8")
    table = parse_csv(csv_file)
    csv_file.close()

    return table