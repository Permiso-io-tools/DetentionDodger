import os

from core.Other.Arguments.ArgParse import parseArgs
from core.Other.PrintOutput.PrintOutput import printOutput
from core.Authentication.Authentication import authenticate
from core.Resources.MainActivity.MainActivity import MainActivity

args = parseArgs()

if not os.path.exists("./output"):
    os.mkdir("./output")

profile = args.profile
accountid = None
user = args.user

try:
    accountid = authenticate(
        Profile=profile,
        AccessKey=None,
        SecretKey=None,
        SessionToken=None,
        Service="sts",
        UserAgent=None
    ).get_caller_identity()['Account']

    printOutput(f"Testing Account {accountid}", "loading")

except Exception as e:
    printOutput(f"Error with credentials provided: {str(e)}", "error")
    exit()

if accountid is None:
    printOutput(f"Error with credentials provided", "error")
    exit()

if not os.path.exists(f'./output/{accountid}'):
    os.mkdir(f"./output/{accountid}")

mainactivity = MainActivity(profile=profile, accountID=accountid, user=user)
mainactivity.main_activity()

