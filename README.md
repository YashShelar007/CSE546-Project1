# CSE546-Project1

Group members:

Yash Shelar

Sougata Nayak

Anvita Lingampalli



Tasks:

Yash Shelar:
- Implemented functionality for SQS request and response queues
- Created autoscaling policy
- Set up cloud watch alarms

Sougata Nayak:
- Implemented the App tier code
  - fetching images from sqs queues and running classification algorithm
  - Stored the results in S3 output bucket and sending those back to reponse queue
  
 Anvita Lingampalli:
 - Implemented the code which receives the image files from workload generator
 - Store the images in S3 input bucket.
 - Recieve response from the request queue and display. 


 
 AWS credentials:
 
 access_key= 
 
 secret_key= 
 
 
 PEM key: cloudcrowd
 
 
 Webtier URL: 100.25.3.37:3000
 
 
 SQS request queue: cloudCrowd-request
 
 SQS response queue: cloudCrowd-response
 
 
 S3 input bucket: cloudcrowd-input
 
 S3 output bucket: cloudcrowd-output
 
 
 
 
 
  
