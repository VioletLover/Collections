import json
import csv
import MySQLdb as db

# csv to json
def read_csv(file):
    csv_rows = []
    with open(file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]]} for i in range(len(title))])
            return csv_rows
def write_json(data, json_file, format=None):
    with open(json_file) as f:
        if format == 'good':
            f.write(json.dumps(data, sort_keys=False, ident=4, separators=(',', ':'), encoding='utf-8', ensure_ascii=False))
        else:
            f.write(json.dumps(data))
# implement
write_json(read_csv('test.csv'), 'output.json', 'good')


# json to csv
def read_json(filename):
    return json.loads(open(filename).read())
def write_csv(data,filename):
    with open(filename) as outf:
        writer = csv.DictWriter(outf, outf[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
# implement
write_csv(read_json('test.json'), 'output.csv')







