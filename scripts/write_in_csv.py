import csv

def write_data_to_csv(year, org_data):

    csv_file_path = f'data/{year}.csv'
    fields = ['Organization', 'Technologies', 'Topics', 'Selected_Students']

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        # Write the header
        csv_writer.writeheader()
        
        sorted_org_data = sorted(org_data, key=lambda item: item['Selected_Students'], reverse=True)

        # Write the data
        csv_writer.writerows(sorted_org_data)

    print(f'Data has been stored in {csv_file_path}')