import os, uuid
import csv, json, yaml


# Common parameters:
folder = os.path.join(os.getcwd(), 'lesson_2')
out_csv_file = os.path.join(os.getcwd(), 'lesson_2', 'result.csv')
out_json_file = os.path.join(os.getcwd(), 'lesson_2', 'orders.json')
out_yaml_file = os.path.join(os.getcwd(), 'lesson_2', 'sample.yml')


def get_data(file, header):
    with open(file, mode='r', encoding='utf-8-sig') as f_d:
        rows = f_d.read().split('\n')
    rows = tuple(filter(lambda row: any(field in row for field in header), rows))
    rows = tuple([row.replace(field, '').strip() for field in header for row in rows if field in row])
    return rows


def save_to_csv(data, file):
    with open(file, 'w', encoding='utf-8', newline='') as f_d:
        out_csv = csv.writer(f_d, delimiter=',', quoting=csv.QUOTE_ALL)
        out_csv.writerow(csv_header)
        [out_csv.writerow(line) for line in data]


def write_orders_to_json(**kwargs):
    with open(out_json_file, 'r') as f_d:
        orders = json.load(f_d)
    with open(out_json_file, 'w') as f_d:
        orders['orders'].append(kwargs)
        json.dump(orders, f_d, sort_keys=True, indent=2)


# CSV task:
ext_fltr = '.txt'
csv_header = (
    'Изготовитель системы',
    'Название ОС',
    'Код продукта',
    'Тип системы',
    )

input_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(ext_fltr)]
csv_header = [field + ':' for field in csv_header if not field.endswith(':')]
data = [get_data(file, csv_header) for file in input_files]
save_to_csv(data, out_csv_file)
print('CSV task completed')


# JSON task:
write_orders_to_json(
    uuid=str(uuid.uuid4()),
    item='Judas conscience', 
    quantity=1, 
    price=30, 
    currency='Tyrian Shekel',
    buyer='Romanian Empire', 
    date='0033-04-03')
write_orders_to_json(
    uuid=str(uuid.uuid4()),
    item='USSR citizens', 
    quantity=288600000, 
    price=1000000, 
    currency='USD', 
    buyer='North Atlantic Treaty Organization', 
    date='1990-10-15')
print('JSON task completed')


# YAML task:
sample = {
    'a': [1, '2', 3.14159, '£'],
    'b': 1000000,
    'c': {
        'α': 'Α',
        'β': 'Β',
        'γ': 'Γ',
        'δ': 'Δ',        
    }
}
with open(out_yaml_file, 'w', encoding='utf-8') as f_d:
    yaml.safe_dump(sample, f_d, default_flow_style=False, allow_unicode=True)
with open(out_yaml_file, 'r', encoding='utf-8') as f_d:
    loaded = yaml.load(f_d, Loader=yaml.SafeLoader)
    if sample == loaded:
        print('YAML task completed, data is correct.')
    else:
        print('YAML task completed, data is wrong.')