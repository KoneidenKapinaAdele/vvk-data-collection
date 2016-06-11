
from json import load
from csv import writer

def json_fields(data):
    return list(reduce(lambda set1, set2: set1.union(set2),
            (set(record.keys()) for record in data)))

def pick_fields(fields, record):
    return [record.get(field, None) for field in fields]

def json_to_table(fields, data):
    return (pick_fields(fields, record) for record in data)

def write_csv(f, fields, rows):
    csv = writer(f)
    csv.writerow(fields)
    csv.writerows(rows)

def pipe(infile, outfile):
    json = load(infile)
    fields = json_fields(json)
    rows = json_to_table(fields, json)
    write_csv(outfile, fields, rows)

if __name__ == '__main__':
    from sys import stdin, stdout
    pipe(stdin, stdout)

