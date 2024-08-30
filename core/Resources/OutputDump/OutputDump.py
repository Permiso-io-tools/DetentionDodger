import csv
from core.Other.PrintOutput.PrintOutput import printOutput

def dumpCSV(result, outputdir, username):
    csvfile = csv.writer(open(f'./output/{outputdir}/{username}.csv', "w"))
    csvfile.writerow(["Scenario", "Status", "Allowed", "Denied"])
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for row in result:
        csvfile.writerow(row.values())
    #writer.writeheader()
    #del (result[0])
    printOutput(f"Outputfile ./output/{outputdir}/{username}.csv successfully created", "success")
