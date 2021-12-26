# AM_test_2: CRM REST API

This is a simple CRM REST API application developed using Django Rest Framework
for the second stage of The Agile Monkeys recruitment process. This API is designed to
handle a database of Users and Customers and manage them using CRUD methods.

This README file describes how to deploy this web application, the functionalities it
implements, and how to use them

# Download

You can download this repository using [Git](https://git-scm.com/) with the following command:
```
git clone https://github.com/mjonian93/AM_test_2
```

# Deployment

This applications is dependant on some Python libraries specified in the requirements.txt
file. To ease the deployment, a Dockerfile is included which automates app deployment.
To build the container, [Docker](https://docs.docker.com/engine/install/) must 
be installed first. Once this requirement is satisfied, open a terminal, navigate to the 
root repository directory (the one that contains the Dockerfile) and run the
following command to create a Docker image (we will name it docker-amcrm-v1.0):
```
docker build . -t docker-amcrm-v1.0
```
Once the image has been created, you can start the container by executing:
```
docker run docker-amcrm-v1.0
```
Check the container has been created with `docker ps`.


# API Models

# Using the API





