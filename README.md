### Raspberry Pi Sensor Web App running on AWS

#### AWS Services Used:
- IoT Core
- Lambda
- RDS (MySQL)
- EC2
- SNS/SES (in development, so the sensors can communicate in case they fail or run into some other unexpected error)
- Auto Scaling Group
- Elastic Load Balancing
- CodeDeploy

#### Hardware Used:
- 2 x Raspberry Pi 3B+
- 2 x DHT22 Sensors

#### How it works:
- Two Raspberry Pi's read DHT22 sensors every 5 minutes and send the data via MQTT to AWS IoT where Lambda functions are triggered. 
- The Lambda functions read the data from AWS IoT and inserts the data into a MySQL RDS instance.
- The web app is deployed in an Auto Scaling Group with an Application Load Balancer sitting in front.
