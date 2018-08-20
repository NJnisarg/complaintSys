# Introduction

This application is built for the complaint management system. This application is a complete RESTful Backend with non-HTML views but views in form of JSON Data being exchanged from API Calls.

# Installation and Usage

- Unzip the Repo :
```
    tar xf Task_2.tar.gz
```

- Start a virtualenv
```
    virtualenv -p python3 Env2
    source Env2/bin/activate
```

- change dir into the folder named complaintSys and containing the `manage.py` file.

- install all the dependencies
```
    pip install -r requirements.txt
```

- Make migrations and start the server for testing
```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
```

- The Above steps starts the server(with http) on localhost:8000. Go to `http://localhost:8000/` in your browser(preferably chrome). Since this backend is a RESTful service based backend, all the APIs can be tested using API test tools like `postman`.
- For getting `postman`. Please have a look at `https://www.getpostman.com/`

# APIs implemented
- Base Url: `http://localhost:8000`
### Complaint APIs
- `/api/complantAPI/get_all_complaints/`
	- GET request
	- Returns all the complaint objects if you are a resolver. And returns all the complaints made by a user if you are a user role.
- `/api/complantAPI/get_complaint/<pk>/`
	- Passed the Id of a complaint as the path variable called `pk`. Retrives a single complaint object.
- `/api/complantAPI/get_comp_by_user/<pk>/`
	- GET Request
	- Passes the Id of the user for getting all the complaints associated with that account. pk is the Id of the user.
- `/api/complantAPI/get_comp_by_tag/<pk>/`
	- GET Request
	- Pass the name of the tag for which you want to retrieve the compaints made. tag name = pk.
	- Here if the user is resolver, then all complaints under that tag are returned. If the user is a normal user then only his complaints for the tag are returned.
- `/api/complantAPI/get_complaint_resolved`
	- GET Request
	- Gets all the resolved complaints. For a normal user it gets all complaints resolved made by him.
- `/api/complantAPI/get_complaint_unresolved`
	- GET Request
	- Gets all the unresolved complaints. For a normal user it gets all complaints unresolved made by him.
- `/api/complantAPI/create_tag/`
	- POST Request
	- Creates a new tag(category) for complaint.
	- Only resolver allowed to do that
	- Request body:
		- "name":"string"
- `/api/complantAPI/get_all_tags/`
	- GET Request
	- Gets all the tags in the database
- `/api/complantAPI/generate_complaint/`
	- POST Request
	- Used to create a new complaint. Only normal user allow access.
	- Request :
		- "complainant": "string"
		- "title":"string",
		- "description":"String",
		- "tag":"string"
	- response :
		- Complaint object created with above data and extra information like timestamp and `status`(=True or =False)
- `/api/complantAPI/update_complaint_data/<pk>/`
	- PUT Request
	- Pass the pk= id of the complaint to update
	- Request:
		- "complainant": "string"
		- "title":"string",
		- "description":"String",
		- "tag":"string"
	- response :
		- Complaint object updated with above data and extra information like timestamp and `status`(=True or =False)
- `/api/complantAPI/resolve_complaint/<pk>/`
	- PUT request
	- Pass the pk= complaint id
	- Pass no content.
	- Returns status 202 if successfully resolved and changes the `status` to `True`. Returns 204 if already resolved.
- `/api/complantAPI/add_comment/<pk>/`
	- PUT Request
	- pass the pk = complaint id
	- Request:
		- "comment" : "string"
	- Response:
		- The Updated complaint object.

### Authentication APIs
- `/Auth/register/user/`
	- POST API call
	- Request:
		- "username":"string",
		- "password":"string"
	- Response:
		- User credentails and a field called `type` with value `user` and with a token for further api calls. The token has to be passed in as `Authorization` header in for of `Token <token>`
- `/Auth/register/resolver/`
	- POST API call
	- Request:
		- "username":"string",
		- "password":"string"
	- Response:
		- User credentails and a field called `type` with value `resolver` and with a token for further api calls. The token has to be passed in as `Authorization` header in for of `Token <token>`
- `/Auth/login`
	- POST API call
	- Same request object as register object
	- Same response as register request


# Features Implemented
- A user management system with 2 roles : 1.) resolver 2.) user. Permissioned access to APIs based on the role of the user.
- Token based authentication system for RESTful api calls
-  Based on the `role` of the user logged in(passing the token), the API behaves and takes the right step for that user.
-  The complaint API has a system to categorize and filter complaints based on `tags`.
-  The APIs also allow a way to add comments by the resolver.

# Database Schema:

### Complaint(Table/Data object)
- 	complainant
- 	respondent
- 	title
- 	description
- 	status
- 	tag
- 	createdOn
- 	comment

### Tag(Table/ Data object)
- name (tag name, also the primary key)

### User
- Inbuilt Django User object
- Username
- Password
- Group(=role)
- Token


# Author

- Nisarg S. Joshi
