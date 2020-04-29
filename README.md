# Azure Machine Learning 

### Architecture

![alt text](./architecture.PNG "Logo Title Text 1")

* MailSender  
  - Trigger: Time Trigger
  - Action: Send mail to a user with a link to avoid Compute Instance shutdown
  - Services: SendGrid

* CancelShutDown  
  - Trigger: HTTP Trigger
  - Action: Add an entry on Azure Table Storage to cancel compute instance shutdown, triggered by user interaction with mail
  - Services: Azure Table Storage

* ComputeShutdown  
  - Trigger: Time Trigger
  - Action: Perform compute instance shutdown if no entry is found in the Azure Table Storage
  - Services: Azure Table Storage, Azure Machine Learning
