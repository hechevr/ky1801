import numpy as np
import csv
from chord_lib import chord_id

# root list
root_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
type_list = ['m', '', 'aug', 'dim', 'sus2', 'sus4']

def main():
    # call function to return chord
    table = []
    for i in root_list:
        table.append([i, ''])
        for j in type_list:
            row = [j]
            result = chord_id(i, j)
            row.append(result)
            table.append(row)
    # write chord table to csv file
    with open('output.csv', 'w') as fo:
        writer = csv.writer(fo)
        for row in table:
            writer.writerow(row)

if __name__ == '__main__':
    main() 
