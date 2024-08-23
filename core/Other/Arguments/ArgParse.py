import argparse

from core.Other.Arguments.Banner import printBanner


def parseArgs():
    printBanner()
    parser = argparse.ArgumentParser(
        prog='DetentionDodger',
        description='DetentionDodger is a tool designed to find users whose credentials have been leaked/compromised and the impact they have on the target',
    )

    parser.add_argument('-p', '--profile', help="The AWS Profile Name to authenticate as. Default is 'default'. The credentials need to have access to iam:ListUsers, iam:ListUserPolicies, iam:ListAttachedUserPolicies, iam:ListGroupsForUser, iam:ListGroupPolicies, iam:ListAttachedGroupPolicies, cloudtrail:LookupEvents, iam:GetPolicyVersion, iam:GetPolicy", default="default")
    parser.add_argument('-u', '--user', help="The AWS User to test. If not set, a list of users will be ")
    #parser.add_argument('-sl', '--search-logs', help="Search logs for attempt to run iam:ListAttachedUserPolicies", action="store_true")

    return parser.parse_args()

