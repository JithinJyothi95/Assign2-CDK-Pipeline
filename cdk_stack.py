import os
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
)
# from aws_cdk.aws_lambda_nodejs import NodejsFunction
# from aws_cdk.aws_lambda import Runtime  
from constructs import Construct


class DailyMoodTrackerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        print("Inside DailyMoodTrackerStack")

        bucket = s3.Bucket(self, "JJMoodLogs8876281",
            bucket_name="jj-mood-logs-8876281",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        table = dynamodb.Table(self, "DailyMoodTable8876281",
            table_name="daily_mood_8876281",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

        print("Bucket name:", bucket.bucket_name)
        print("Lambda path exists:", os.path.exists("lambda"))
        print("Handler file exists:", os.path.exists("lambda/moodHandler.js"))

        lambda_fn = _lambda.Function(self, "LogMoodFunction8876281",
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="moodHandler.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        table.grant_read_write_data(lambda_fn)

        api = apigateway.LambdaRestApi(
            self, "MoodLoggerAPI",
            handler=lambda_fn,
            proxy=False,
            rest_api_name="Mood Logging API"
        )

        moods = api.root.add_resource("moods")
        moods.add_method("POST")
        moods.add_method("GET")
        moods.add_method("DELETE")

        CfnOutput(self, "MoodLoggerAPIEndpoint", value=f"{api.url}moods")
        CfnOutput(self, "LambdaFunctionName", value=lambda_fn.function_name)
        CfnOutput(self, "DynamoDBTableName", value=table.table_name)
        CfnOutput(self, "S3BucketName", value=bucket.bucket_name)
        print("Stack initialized successfully with the following resources:")
        print(f"API Endpoint: {api.url}moods")
        print(f"Lambda Function Name: {lambda_fn.function_name}")
        print(f"DynamoDB Table Name: {table.table_name}")
        print(f"S3 Bucket Name: {bucket.bucket_name}")