import csv, argparse, os

from remove_bom_inplace import remove_bom_inplace
from decimal import Decimal

# main
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='location of the csv to convert')

args = parser.parse_args()

remove_bom_inplace(args.path)


# read input csv file
with open(args.path, 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

results = []

# transform the data
for row in rows:
    # skip pending transactions
    if (row['Transaction Status'] == 'PENDING'):
        continue

    # parse and convert the transaction amount
    input_amount: str = row['Transaction Amount'].replace("$", "")
    amount_val = Decimal(input_amount).quantize(Decimal('.01'))
    # monarch wants the transaction negated so that it correctly understands the transaction
    negated_amount = -1 * amount_val
    output_amount = str(negated_amount)

    # fix the dates to the format that Monarch wants
    input_date = row['Transaction Date']
    [month, day, year] = input_date.split('/')
    output_date = f'{year}-{month}-{day}'

    output_dict = {
        'Date': output_date,
        'Merchant': row['Transaction Merchant Name'],
        'Category': row['Merchant Category Group Name'],
        'Account': '',
        'Original Statement': '',
        'Notes': '',
        'Amount': output_amount,
        'Tags': ''
    }

    results.append(output_dict)

# write the data to a new csv
_, output_file_name = os.path.split(args.path)

with open(f'output/{output_file_name}', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    
    # Write the column names
    writer.writeheader()
    
    # Write the rows
    writer.writerows(results)

