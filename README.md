# Capstone: Trivia API with Authentication via Auth0


## General Introduction
Capstone project for Udacity Full Stack Developer Nanodegree. Project is an API using Flask, written in python and leverages Auth0 for endpoint authentication. API returns data in JSON format. Leverages flask-migrate for database migrations.


## Running Locally and Installing Dependencies
To run the app locally, follow these steps:
* clone the repo
* `cd app`
* create a python virtual environment with `virtualenv env`
* activate your environment with `source env/bin/activate`
* install dependencies with `pip3 install -r requirements.txt`
* in models.py, define a `database_name` and `database_path`
* setup an Auth0 application, API and roles. More details in Auth0 Configuration section below.
* in auth.py, define a `AUTH0_DOMAIN` `ALGORITHMS` and `API_AUDIENCE`
* run the application with `sh launch.sh`. You might need to `chmod +x launch.sh` in order to run it.
* you can run `sh bootstrap.sh` to load your local database with data. Edit with your table name.


## Auth0 Configuration
* Create an application of type `Single Page Application`
* Create an API, with RBAC enabled. Also enable `add permissions to access token` setting. Add the following API permissions:
  * get:questions
  * get:categories
  * delete:questions
  * post:questions
  * patch:questions
  * post:categories
* Setup roles per your desired permission sets
* You will define a `AUTH0_DOMAIN` `ALGORITHMS` and `API_AUDIENCE` based on the above configurations in auth.py as part of running locally.


## Tests
Automated tests require an auth token. In `test_flaskr.py` provide an auth token and set `admin` variable to `True` or `False` based on whether token user is admin role.

To run tests, run `sh run_tests.sh`. This will wipe test database, recreate database and run tests. Tests are done using unittest.

You might need to `chmod +x run_tests.sh` in order to run it.


## Deployment
App can be deployed easily on Heroku and using gunicorn. Instructions below assume you have installed Heroku CLI and have an account.
* create heroku app `heroku create name_of_your_app`
* add remote with `git remote add heroku heroku_git_url`
* setup postgres with `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
* get your `database_path` with `heroku config --app name_of_your_application`
* add the `database_path` and your Auth0 information to `setup.py`
* deploy with `git push heroku master`
* make sure your environment variables from `setup.py` are defined in the project environment variables.
* enjoy!


## Live Demo
The application is deployed at: [https://trivia-api-jeff.herokuapp.com/](https://trivia-api-jeff.herokuapp.com/).

To generate an auth token (jwt), go to [https://nacler.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=bnPnm6NHbJGg8mZlKmg64yk3wW3d0HW1&redirect_uri=http://localhost:8080/login-results](https://nacler.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=bnPnm6NHbJGg8mZlKmg64yk3wW3d0HW1&redirect_uri=http://localhost:8080/login-results) in your browser and enter the credentials below. You will need to include this bearer token in your requests. See section *Example Requests and Responses* for request examples.

*Admin Role Credentials*
user: `admin@trivia-api.com`
pass: `P@ssword123`

*User Role Credentials*
user: `user@trivia-api.com`
pass: `P@ssword123`

The deployed application has the follwing roles and permissions: **Admin** and **User**

Admins can:
* get:questions
* get:categories
* delete:questions
* post:questions
* patch:questions
* post:categories

Users can:
* get:questions
* get:categories


## Postman
Included in a postman collection you can use to hit the endpoints. Adjust the host variable in the mail `Trivia API` folder. Set your Admin and User bearer token in the `Admin` and `User` folders. Hitting endpoints that require admin permissions with a user token should return a 403.


## Endpoints
The following are endpoints for the service:
* `GET /questions`
* `GET /categories`
* `POST /questions`
* `POST /categories`
* `PATCH /questions/<question_id>`
* `DELETE /questions/<question_id>`


## Example Requests and Responses

#### GET /questions
Local Request:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/questions`

Deployed Request:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://trivia-api-jeff.herokuapp.com/questions`

Example Response:
```
{
    "questions": [
        {
            "answer": "Maybe",
            "category": "3",
            "difficulty": 3,
            "id": 2,
            "question": "Could this possibly work?"
        },
        {
            "answer": "42",
            "category": "4",
            "difficulty": 2,
            "id": 3,
            "question": "What is the meaning of life?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

#### GET /categories
Local Request:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/categories`

Deployed Request:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://trivia-api-jeff.herokuapp.com/categories`

Example Response:
```
{
    "categories": {
        "1": "Funny",
        "2": "Sports",
        "3": "History",
        "4": "Drama",
        "5": "Entertainment"
    },
    "success": true
}
```

#### POST /questions
Local Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  http://127.0.0.1:5000/questions
```

Deployed Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  https://trivia-api-jeff.herokuapp.com/questions
```

Example Response:
```
{
    "new_question": 3,
    "success": true
}
```

#### POST /questions (with search)
Local Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"searchTerm": "<search_string>"}' \
  http://127.0.0.1:5000/questions
```

Deployed Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"searchTerm": "<search_string>"}' \
  https://trivia-api-jeff.herokuapp.com/questions
```

Example Response:
```
{
    "questions": [
        {
            "answer": "42",
            "category": "4",
            "difficulty": 2,
            "id": 4,
            "question": "What is the meaning of life?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### POST /categories
Local Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"type": "<category_name>"}' \
  http://127.0.0.1:5000/categories
```

Deployed Request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"type": "<category_name>"}' \
  https://trivia-api-jeff.herokuapp.com/categories
```

Example Response:
```
{
    "new_category": 6,
    "success": true
}
```

#### DELETE /questions/<question_id>
Local Request:
```
curl --request DELETE \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://127.0.0.1:5000/questions/<question_id>
```

Deployed Request:
```
curl --request DELETE \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  https://trivia-api-jeff.herokuapp.com/questions/<question_id>
```

Example Response:
```
{
    "success": true
}
```

#### PATCH /questions/<question_id>
Local Request:
```
curl --header "Content-Type: application/json" \
  --request PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  http://127.0.0.1:5000/questions/<question_id>
```

Deployed Request:
```
curl --header "Content-Type: application/json" \
  --request PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  https://trivia-api-jeff.herokuapp.com/questions/<question_id>
```

Example Response:
```
{
    "question": 3,
    "success": true
}
```
