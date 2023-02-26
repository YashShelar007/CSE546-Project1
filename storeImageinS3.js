require("dotenv").config();
const S3 = require("aws-sdk"); //s3 from our aws
const fs = require("fs");



const bucket = "cloudcrowd-input" //name of our s3 bucket
const region = "us-east-1"

const s3 = new S3({region,})

function storeImage(imagefile){
    const fstream = fs.readFileSync(imagefile)

    const params = {
        Bucket: bucket,
        Body: imagefile,
        Key: fstream, //name
    };

    return s3.upload(params).promise();
}