import json

from core.Other.PrintOutput.PrintOutput import printOutput
import os
import prettytable
from termcolor import colored
from tabulate import tabulate
class TablePrint():
    def tableprint(self, queryResult):
        allfields = []
        fieldNames = None

        scenariolength = 0
        statuslength = 0
        allowlength = 0
        denylength = 0
        csvdata = []
        returndata = [["Scenario", "Status", "Allowed", "Denied"]]

        for scenarioname, scenariostatus in queryResult.items():
            fieldNames = {"Scenario": "", "Status": "", "Allowed": "", "Denied": ""}

            fieldNames['Scenario'] = scenarioname
            csvdata.append(scenarioname)
            if len(scenarioname) > scenariolength:
                scenariolength = len(scenarioname)

            if scenariostatus['status'] == "allowed":
                fieldNames["Status"] = colored(scenariostatus['status'], "green")
            if scenariostatus['status'] == "denied":
                fieldNames["Status"] = colored(scenariostatus['status'], "red")
            if scenariostatus['status'] == "partially":
                fieldNames["Status"] = colored(scenariostatus['status'], "yellow")

            csvdata.append(scenariostatus['status'])

            if len(scenariostatus['status']) > statuslength:
                statuslength = len(scenariostatus['status'])


            allowessc = ""
            for scallow in scenariostatus['allowed']:
                if len(scallow) > allowlength:
                    allowlength = len(scallow)

                allowessc += scallow + "\n"
            fieldNames['Allowed'] = allowessc
            csvdata.append(allowessc)

            denessc = ""
            for scden in scenariostatus['denied']:
                if len(scden) > denylength:
                    denylength = len(scden)
                denessc += scden + "\n"
            fieldNames['Denied'] = denessc
            csvdata.append(denessc)

            allfields.append(fieldNames)
            returndata.append(csvdata)

        if len(fieldNames) == 1:
            printOutput(
                "No values for this query",
                "success"
            )

        else:

            # print(tabulate(queryResult, headers='keys', tablefmt='psql'))
            column_width, row_width = os.get_terminal_size(0)
            maxwidth = int(os.get_terminal_size().columns / 3)
            table = prettytable.PrettyTable(
                max_table_width=column_width,
                align='l',
                field_names=fieldNames.keys(),
                max_width=maxwidth
            )
            table.set_style(prettytable.DOUBLE_BORDER)
            for row in allfields:
                table.add_row(row.values())
                table.add_row(["="*scenariolength, "="*statuslength, "="*allowlength, "="*denylength])

            rows = []
            for row in allfields:
                rows.append(row.values())

            #print(tabulate(rows, headers=list(fieldNames.keys()), tablefmt="outline"))
            print(table)
        printOutput('-' * (os.get_terminal_size().columns - 10), "success")

        return returndata