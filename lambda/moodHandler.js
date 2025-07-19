const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const {
  DynamoDBDocumentClient,
  PutCommand,
  QueryCommand,
  DeleteCommand
} = require("@aws-sdk/lib-dynamodb");

const client = new DynamoDBClient();
const docClient = DynamoDBDocumentClient.from(client);

const tableName = process.env.TABLE_NAME;

exports.handler = async (event) => {
  console.log("Event:", JSON.stringify(event, null, 2));

  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE"
  };

  try {
    const method = event.httpMethod;

    if (method === "OPTIONS") {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: "CORS preflight" })
      };
    }

    if (method === "POST") {
      if (!event.body) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ message: "Missing request body" })
        };
      }

      const body = JSON.parse(event.body);
      const { user_id, mood, timestamp } = body;

      if (!user_id || !mood || !timestamp) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ message: "Missing user_id, mood, or timestamp" })
        };
      }

      const params = {
        TableName: tableName,
        Item: { user_id, timestamp, mood }
      };

      await docClient.send(new PutCommand(params));

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: "Mood logged!" })
      };
    }

    if (method === "GET") {
      const user_id = event.queryStringParameters?.user_id || "demo_user";

      const params = {
        TableName: tableName,
        KeyConditionExpression: "user_id = :uid",
        ExpressionAttributeValues: { ":uid": user_id }
      };

      const data = await docClient.send(new QueryCommand(params));

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data.Items)
      };
    }

    if (method === "DELETE") {
      if (!event.body) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ message: "Missing request body" })
        };
      }

      const body = JSON.parse(event.body);
      const { user_id, timestamp } = body;

      if (!user_id || !timestamp) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ message: "Missing user_id or timestamp" })
        };
      }

      const params = {
        TableName: tableName,
        Key: { user_id, timestamp }
      };

      await docClient.send(new DeleteCommand(params));

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: "Mood entry deleted" })
      };
    }
// Method not allowed
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ message: "Method not allowed" })
    };

  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ message: "Internal server error", error: error.message })
    };
  }
};
