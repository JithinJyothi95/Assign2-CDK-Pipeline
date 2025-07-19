import aws_cdk as cdk
from cdk_stack import DailyMoodTrackerStack

app = cdk.App()
# Create the stack
DailyMoodTrackerStack(app, "DailyMoodTrackerStackJJ8876281")

app.synth()
