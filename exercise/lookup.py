import csv
import sys

def load_table():
    table = []
    with open("output.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # print(row)
            if (len(row[1]) == 0):
                title = row[0]
            else:
                row[0] = title + " " + row[0]
                table.append(row)
    return table

def lookup(s, table):
    data = []
    for t in table:
        if s in t:
            # print(t)
            data.append(s)
    return data

def lookupA(s):
    table = load_table()
    return lookup(s, table)

if __name__ == "__main__":
    table = load_table()
    lookup(sys.argv[1], table)
