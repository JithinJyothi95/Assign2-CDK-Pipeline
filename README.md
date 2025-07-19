# Daily Mood Tracker (CDK + CodePipeline)
**Author**: Jithin Jyothi  
**Student ID**: 8876281  

## Project Purpose
This project logs daily mood entries into a DynamoDB table using a Lambda function. It is automatically deployed using AWS CodePipeline and AWS CDK.

## Resources Created
- **S3 Bucket**: `jj-mood-logs-8876281`
- **DynamoDB Table**: `daily_mood_8876281`
- **Lambda Function**: Logs mood entries with timestamp

## CI/CD Flow
- Source: GitHub repository
- Build/Deploy: CodeBuild using `buildspec.yml`

## Screenshots
_Add screenshots from AWS Console here showing:_
1. S3 bucket
2. Lambda function
3. DynamoDB table
4. CodePipeline execution

## Project Structure
```
.
├── app.py
├── cdk_stack.py
├── buildspec.yml
├── lambda/
│   └── moodHandler.js
├── requirements.txt
├── .gitignore
└── README.md
```
