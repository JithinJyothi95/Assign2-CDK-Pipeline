#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_stack import DailyMoodTrackerStack

app = cdk.App()
DailyMoodTrackerStack(app, "DailyMoodTrackerStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
)

app.synth()

