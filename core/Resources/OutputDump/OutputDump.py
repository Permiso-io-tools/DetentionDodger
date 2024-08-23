import csv
from core.Other.PrintOutput.PrintOutput import printOutput

def dumpCSV(result, outputdir, username):
    with open(f'./output/{outputdir}/{username}.csv', 'w') as csvfile:
        fieldnames = result[0]
        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer = csv.writer(csvfile, delimiter=',')
        #writer.writeheader()
        #del (result[0])
        writer.writerows(result)
        csvfile.close()
    printOutput(f"Outputfile ./output/{outputdir}/{username}.csv successfully created", "success")
