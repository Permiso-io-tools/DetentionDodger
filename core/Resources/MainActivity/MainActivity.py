from core.Other.PrintOutput.PrintOutput import printOutput
from core.Other.TablePrint import TablePrint
from core.Resources.IAM.BypassCheck import BypassCheck
from core.Resources.CloudTrail.FindQuarantineAttachment import FindQuarantineAttachment
import json
from core.Resources.OutputDump.OutputDump import dumpCSV

class MainActivity:
    def __init__(self, profile, accountID, user):
        self.bypassCheckObj = BypassCheck(profile=profile)
        self.cloudTrailObj = FindQuarantineAttachment(profile=profile)
        self.accountID = accountID
        self.user = user
    def main_activity(self, checkall):
        if checkall:
            scenariofile = "scenarios/allservices.json"
        else:
            scenariofile = "scenarios/scenarios.json"

        with open(scenariofile) as scenariosfile:
            SCENARIOS = json.load(scenariosfile)

        if self.user is None:
            users = self.bypassCheckObj.list_compromised_users()
        else:
            users = [self.user]

        if users is not None and len(users) > 0:
            for user in users:
                printOutput("----------------------------------------------------", type="loading")
                printOutput(f"           {user}", type="loading")
                printOutput("----------------------------------------------------", type="loading")
                policyDefinition = {
                    "Policies": []
                }

                userPermissionBoundary = self.bypassCheckObj.get_user_permission_boundary(user)

                if userPermissionBoundary is not None:
                    userPermissionBoundary = [json.dumps(userPermissionBoundary)]

                attachedPolices = self.bypassCheckObj.get_attached_user_policies(user)
                if attachedPolices is not None:
                    policyDefinition["Policies"] = attachedPolices

                inlinePolices = self.bypassCheckObj.get_user_inline_policies(user)
                if inlinePolices is not None:
                    policyDefinition["Policies"].extend(inlinePolices)

                groups = self.bypassCheckObj.get_user_groups(user)
                if groups is not None:
                    for group in groups:
                        groupAttachedPolices = self.bypassCheckObj.get_attached_group_policies(group)
                        if groupAttachedPolices is not None:
                            policyDefinition["Policies"].extend(groupAttachedPolices)

                        groupPolices = self.bypassCheckObj.get_group_inline_policies(group)
                        if groupPolices is not None:
                            policyDefinition["Policies"].extend(groupPolices)

                #userPolicies[user] = policyDefinition
                stringPolicies = []
                for policy in policyDefinition['Policies']:
                    stringPolicies.append(json.dumps(policy))
                evaluationResponse = self.bypassCheckObj.find_permissions_in_policy(policyDocumentList=stringPolicies, permissionBoundaryList=userPermissionBoundary, SCENARIOS=SCENARIOS, checkall=checkall)

                tablePrintObj = TablePrint()
                userfields = tablePrintObj.tableprint(evaluationResponse)
                dumpCSV(userfields, self.accountID, user, checkall)

