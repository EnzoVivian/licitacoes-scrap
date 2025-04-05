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

import os
import json
import re
from pathlib import Path
import csv

def check_classification(input_path, output_path):
    existing_data = read_csv_dict(input_path)
    for row in existing_data:
        row['ID_SUBCAT'] = ''
        print(row['DS_ITEM'])
    
    filename = os.path.join(Path(__file__).resolve().parent, 'data', 'categories.json')
    with open(filename, 'r') as categ_jsonfile:
        categ_json_str = json.load(categ_jsonfile)
        categ_json_dict = json.loads(categ_json_str)
        # print(categ_json_dict)
        categ_jsonfile.close()
    """with the name of the product, classify its category/subcategory"""

    for row in existing_data:
        # print(row)
        name = row['DS_ITEM']
        print(name)
        try:
            name=name.lower()            
            #look for rule that applies
            for key, categ_type in categ_json_dict.items():
                # print(categ_type['Sub_Name'])
                for rule in categ_type["Regex"]:
                    result=re.search(rule,name.lower())
                    if result is not None:
                        row['ID_SUBCAT'] = key #returns the ID_Subcat of the rule
            # return 1 #returns 1 for "not classified"
            #** IF IT RETURNS 1, 'NOT CATEGORIZED'
            row['ID_SUBCAT'] = 1
        except:
            row['ID_SUBCAT'] = 1
            
    save_csv_dict(existing_data, output_path)
        
def main():
    input_path = "data/2023.csv/pessoa-item2.csv"
    input_path_2 = "licitacoes/2022.csv/item.csv"
    output_path = "data/2022.csv/pessoa-categoria.csv"
    
    check_classification(input_path, output_path)
    #join_csv(input_path, input_path_2, output_path)
    #filter_by_doc_type_dict(input_path output_path)
    #filter_by_best(input_path, output_path)
    #filter_by_doc_type(input_path, output_path)

if __name__ == "__main__":
    main()