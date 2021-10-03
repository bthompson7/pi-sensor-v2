### Raspberry Pi Sensor Web App running on AWS

#### AWS Services Used:
- IoT Core
- Lambda
- EC2
- RDS (MySQL)

#### How it works:
- Two Raspberry Pi's read DHT22 sensors every 5 minutes and send the data via MQTT to AWS IoT where a Lambda function is triggered. 
- The Lambda functions reads the data from AWS IoT and inserts the data into a MySQL RDS instance.
- The web app is deployed on an EC2 instance
