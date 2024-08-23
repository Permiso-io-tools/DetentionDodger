import json
import sys
import datetime

from core.Authentication.Authentication import authenticate
from core.Other.PrintOutput.PrintOutput import printOutput


class FindQuarantineAttachment:
    def __init__(self, profile):
        self.profile = profile
        self.client = authenticate(
            Profile=self.profile,
            AccessKey=None,
            SecretKey=None,
            SessionToken=None,
            UserAgent=None,
            Service="cloudtrail"
        )

    def find_policy_attachment(self):
        printOutput(
            "Finding Policy Attachment Events Attempts with an identity that does not allow iam:AttachUserPolicy",
            "loading"
        )
        startTime = datetime.datetime.now() - datetime.timedelta(days=90)
        try:
            response = self.client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventName',
                        'AttributeValue': 'AttachUserPolicy'
                    }
                ],
                StartTime=startTime
            )
            logs = response['Events']

            while "NextToken" in response:
                response = self.client.lookup_events(
                    LookupAttributes=[
                        {
                            'AttributeKey': 'EventName',
                            'AttributeValue': 'AttachUserPolicy'
                        }
                    ],
                    StartTime=startTime,
                    NextToken=response["NextToken"]
                )
                logs.extend(response['Events'])

            importantEvents = []
            for event in logs:
                user = ""
                policy = ""
                username = event['Username']
                eventData = json.loads(event['CloudTrailEvent'])
                if "errorCode" in eventData and "errorMessage" in eventData:
                    if (
                            (eventData['errorCode'] == "AccessDenied") and
                            (username in eventData['errorMessage'].split(":")[9]) and
                            (eventData['sourceIPAddress'] == "AWS Internal") and
                            (eventData['sourceIPAddress'] == "AWS Internal")
                    ):
                        importantEvents.append(username)
                else:
                    for resource in event['Resources']:
                        if resource['ResourceType'] == "AWS::IAM::User":
                            user = resource['ResourceName']
                        elif resource['ResourceType'] == "AWS::IAM::Policy":
                            policy = resource['ResourceName']

                    if (user == username and
                            (policy == "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV2" or
                             policy == "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV3" or
                             policy == "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantine") and
                            (eventData['sourceIPAddress'] == "AWS Internal") and
                            (eventData['sourceIPAddress'] == "AWS Internal")
                    ):
                        importantEvents.append(username)

            printOutput(f"Found {str(len(importantEvents))} events with quarantine policy attachment", "success")
            return list(set(importantEvents))

        except:
            printOutput(f"Error looking at events: {sys.exc_info()}", "failure")
            return None
