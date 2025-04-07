import os
import csv
import json
import re
from pathlib import Path

def read_csv(input_path):
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    existing_data = []
    header = []
    
    if os.path.exists(input_path) and os.path.getsize(input_path) > 0:
        with open(input_path, "r", encoding="utf-8", newline='') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            existing_data = list(reader)
    
    return existing_data, header

def read_csv_dict(input_path):
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    existing_data = []
    
    if os.path.exists(input_path) and os.path.getsize(input_path) > 0:
        with open(input_path, "r", encoding="utf-8", newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            existing_data = list(reader)
    
    return existing_data

def save_csv(filtered_data, header, output_path):
    if filtered_data:
        with open(output_path, "w", encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(filtered_data)
        print(f"Dados salvos em {output_path}")
    else:
        print("Nenhum registro.")

def save_csv_dict(filtered_data, output_path):
    if filtered_data:
        with open(output_path, "w", encoding="utf-8", newline='') as csv_file:
            fieldnames = filtered_data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_data)
        print(f"Dados salvos em {output_path}")
    else:
        print("Nenhum registro.")

def filter_by_doc_type(input_path, output_path):
    existing_data, header = read_csv(input_path)
    filtered_data = [
        row for row in existing_data
        if len(row) > 4 and row[4] == 'J'
    ]
    save_csv(filtered_data, header, output_path)

def filter_by_doc_type_dict(input_path, output_path):
    existing_data = read_csv_dict(input_path)
    filtered_data = [
        row for row in existing_data
        if row['TP_DOCUMENTO'] == 'J'
    ]
    save_csv(filtered_data, output_path)

def filter_by_best(input_path, output_path):
    existing_data, header = read_csv(input_path)
    filtered_data = [
        row for row in existing_data
        if all(cell != '' for cell in row)
    ]
    save_csv(filtered_data, header, output_path)

def join_csv(input_path, input_path_2, output_path):
    data1 = read_csv_dict(input_path)
    data2 = read_csv_dict(input_path_2)
    
    data2_index = {row['NR_DOCUMENTO']: row for row in data2}
    
    joined_data = []
    for row1 in data1:
        nr_doc = row1['NR_DOCUMENTO']
        if nr_doc in data2_index:
            joined_row = {**row1, **data2_index[nr_doc]}
            joined_data.append(joined_row)
    
    save_csv(joined_data, output_path)

def check_classification(input_path, output_path):
    existing_data = read_csv_dict(input_path)
    filename = os.path.join(Path(__file__).resolve().parent, 'data', 'categories.json')
    with open(filename, 'r') as categ_jsonfile:
        raw_json_str = categ_jsonfile.read()
        if raw_json_str.startswith('"') and raw_json_str.endswith('"'):
            categ_data = json.loads(json.loads(raw_json_str))
        else:
            categ_data = json.loads(raw_json_str)
    compiled_rules = []
    for key, categ_type in categ_data.items():
        for rule in categ_type["Regex"]:
            compiled_rules.append((key, re.compile(rule)))

    for row in existing_data:
        row['ID_SUBCAT'] = 1
        name = row['DS_ITEM'].lower()     
        for subcat_id, regex in compiled_rules:
            if regex.search(name):
                row['ID_SUBCAT'] = subcat_id
                break

    save_csv_dict(existing_data, output_path)
        
def main():
    input_path = "data/2022.csv/pessoa-item.csv"
    input_path_2 = "licitacoes/2022.csv/item.csv"
    output_path = "data/2022.csv/pessoa-categoria.csv"
    
    check_classification(input_path, output_path)
    #join_csv(input_path, input_path_2, output_path)
    #filter_by_doc_type_dict(input_path output_path)
    #filter_by_best(input_path, output_path)
    #filter_by_doc_type(input_path, output_path)

if __name__ == "__main__":
    main()