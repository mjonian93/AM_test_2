# AM_test_2: CRM REST API

This is a simple CRM REST API application developed using Django Rest Framework
for the second stage of The Agile Monkeys recruitment process. This API is designed to
handle a database of Users and Customers and manage them using CRUD methods. The authentication
method implemented in this application is token-based authentication.

This README file describes how to deploy this web application, the functionalities it
implements, and how to use them

# Download

You can download this repository using [Git](https://git-scm.com/) with the following command:
```
git clone https://github.com/mjonian93/AM_test_2
```

# Deployment

This application is dependent on some Python libraries specified in the requirements.txt
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
docker run -p 8000:8000 docker-amcrm-v1.0
```
Check the container has been created with `docker ps`. You can run a terminal in the container
and attach to it using `docker exec -it <container id> /bin/bash`. This is useful to create 
superusers with `manage.py` script. To create a superuser, attach to a terminal
and run the following command:
```
python manage.py createsuper
```

# API Models

This REST API is designed to handle two Object Models: Users (of the application) 
and Customers. The following is a representation of the Models and their fields:

```
User = {
    id = Auto-generated ID Primary Key
    username = String (max-length=32, unique)
    e-mail = String (unique)
    password = String (min-length=8, write-only)
    is_staff = Boolean (default=False)
    }
```
```
Customer = {
    id = Auto-generated ID Primary Key
    name = String (max-length=32)
    surname = String (max-length=32)
    creator = ForeignKey (Creator User)
    last_modifier = Integer (Auto-generated reference to last modifier User)
    image = File (default=None)
    }
```

# Using the API

This sections lists the available URLS in the API and describes how to perform CRUD
operations for authentication and to manage both models.

The CRUD examples shown below have been created using the [HTTPie](https://httpie.io/) tool.

## Urls

These are the URLS available for CRUD operations in the deployed REST API:

```
http://0.0.0.0:8000/api/api-token-auth/ [POST]
http://0.0.0.0:8000/api/users/ [POST, GET]
http://0.0.0.0:8000/api/users/<int:id> [GET, PATCH, DELETE]
http://0.0.0.0:8000/api/customers/ [POST, GET]
http://0.0.0.0:8000/api/customers/<int:id> [GET, PATCH, DELETE]
```

## Authentication
To authenticate in the application, a registered user credentials are required. If there is not any yet, create a 
superuser (required to manage User model, see below). Send a POST request to the assigned endpoint:

```
http post http://0.0.0.0:8000/api/api-token-auth username=<username> password=<password>
```
This request will respond with a JSON Object similar to
```
{
    "token": "<token>"
}
```
Store the given token to use it as authentication mechanism in future requests.

## User Model CRUD
To perform any operation is User model, it is mandatory that the authenticated user has
administrator privileges (is_staff = True). So, authenticate with an admin user to get an
authorized token. You can use a superuser to create Users, if no other user has been created yet.

### Create User
You can create a User with the following command:
```
http POST http://0.0.0.0:8000/api/users/ 'Authorization: Token <token>' username=exampleuser email=exampleuser@example.com password=examplepassword
```
### Retrieve Users/Single User
To obtain a complete register of existing users, run the following command:
```
http GET http://0.0.0.0:8000/api/users/ 'Authorization: Token <token>'
```
To retrieve information about a single user, run the same 
command but pointing to an indexed URL:
```
http GET http://0.0.0.0:8000/api/users/<int:userid> 'Authorization: Token <token>'
```
### Patch User
You can update user fields using the PATCH method, which allows to modify
a Model partially, not being necessary to override every field:
```
http PATCH http://0.0.0.0:8000/api/users/<int:userid> 'Authorization: Token <token>' username=updateduser
```
### Delete User
To delete a user run the DELETE method using the `id` in the URL:
```
http DELETE http://0.0.0.0:8000/api/users/<int:userid> 'Authorization: Token <token>' 
```

## Customer Model CRUD
Similar to the previous, this section encompasses CRUD method examples
but for Customer model, with the addition of image uploading example.
Non-administrator users are able to run CRUD methods on this endpoint.

### Create Customer
To create a customer, run the following command:
```
http POST http://0.0.0.0:8000/api/customers/ 'Authorization: Token <token>' name=examplename surname=examplesurname 
```

### Retrieve Customers/Single Customer
To obtain a complete register of existing customers, run the following command:
```
http GET http://0.0.0.0:8000/api/customers/ 'Authorization: Token <token>'
```
To retrieve information about a single customer, run the same 
command but pointing to an indexed URL:
```
http GET http://0.0.0.0:8000/api/customers/<int:customerid> 'Authorization: Token <token>'
```
### Patch Customer
You can update customers fields with the PATCH command:
```
http PATCH http://0.0.0.0:8000/api/customers/<int:customerid> 'Authorization: Token <token>' name=updatedcustomer
```

### Image upload
To upload an image to a User object, you can use the `--form` 
flag in the request:
```
http --form PATCH http://0.0.0.0:8000/api/customers/<int:customerid> 'Authorization: Token <token>' image@/path/to/image
```
### Delete Customer
To delete a customer run the DELETE method using the `id` in the URL:
```
http DELETE http://0.0.0.0:8000/api/customers/<int:customerid> 'Authorization: Token <token>' 
```


