import csv
from core.Other.PrintOutput.PrintOutput import printOutput

def dumpCSV(result, outputdir, username, checkall):
    if checkall:
        csvfilename = f'./output/{outputdir}/{username}-all-privileges.csv'

    else:
        csvfilename = f'./output/{outputdir}/{username}-predefined-scenarios.csv'

    csvfile = csv.writer(open(csvfilename, "w"))

    csvfile.writerow(["Scenario", "Status", "Allowed", "Denied"])
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for row in result:
        csvfile.writerow(row.values())

    #writer.writeheader()
    #del (result[0])
    printOutput(f"Outputfile {csvfilename} successfully created", "success")
