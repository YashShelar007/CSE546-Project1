const AWS = require("aws-sdk");
AWS.config.update({ region: "us-east-1" });
var sqs = new AWS.SQS({ apiVersion: "2012-11-05" });
const accountID = 707951519696;

function getQueueURL(queueName) {
  print("URL of requested queue");

  var params = {
    QueueName: queueName /* required */,
    QueueOwnerAWSAccountId: accountID,
  };

  const awsRequest = sqs.getQueueUrl(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data); // successful response
  });

  return awsRequest;
}

function getQueueData() {
  print("current queue information");

  var params = {
    QueueUrl: "STRING_VALUE" /* required */,
    AttributeNames: [
      ApproximateNumberOfMessages | LastModifiedTimestamp,
      /* more items */
    ],
  };
  const awsRequest = sqs.getQueueAttributes(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data); // successful response
  });

  return awsRequest;
}

function sendMessage(message, queueURL) {
  print("sent message to the request queue");

  var params = {
    MessageBody: message /* required */,
    QueueUrl: queueURL /* required */,
  };

  const awsRequest = sqs.sendMessage(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data); // successful response
  });

  return awsRequest;
}

function receiveMessage(queueURL) {
  print("receieved message from the response queue");

  var params = {
    QueueUrl: queueURL /* required */,
    MaxNumberOfMessages: 100,
  };

  const awsRequest = sqs.receiveMessage(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data); // successful response
  });

  return awsRequest;
}

function deleteMessage(message, queueURL) {
  print("deleted message from the response queue");

  var params = {
    QueueUrl: queueURL /* required */,
    ReceiptHandle: message /* required */,
  };

  const awsRequest = sqs.deleteMessage(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data); // successful response
  });

  return awsRequest;
}
