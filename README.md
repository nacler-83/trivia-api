# Capstone: Trivia API with Authentication via Auth0


## General Introduction
A simple API in python flask with authentication handled via Auth0. Returns data in JSON format. Leverages flask-migrate for database migrations.


## Running Locally
To run the app locally, follow these steps:
* clone the repo
* `cd app`
* create a python virtual environment with `virtualenv env`
* activate your environment with `source env/bin/activate`
* install dependencies with `pip3 install -r requirements.txt`
* in models.py, define a `database_name` and `database_path`
* setup an Auth0 application, API and roles. More details in Auth0 Configuration section below.
* in auth.py, define a `AUTH0_DOMAIN` `ALGORITHMS` and `API_AUDIENCE`
* run the application with `sh launch.sh`


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
* You will define a `AUTH0_DOMAIN` `ALGORITHMS` and `API_AUDIENCE` in auth.py per running locally instruction


## Tests
To run tests, simply run `sh run_tests.sh`. This will wipe test database, recreate and run tests.


## Live Demo
The application is deployed at: [https://trivia-api-jeff.herokuapp.com/](https://trivia-api-jeff.herokuapp.com/).

You can generate an auth token by hitting [https://nacler.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=bnPnm6NHbJGg8mZlKmg64yk3wW3d0HW1&redirect_uri=http://localhost:8080/login-results](https://nacler.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=bnPnm6NHbJGg8mZlKmg64yk3wW3d0HW1&redirect_uri=http://localhost:8080/login-results) in your browser. You will need to include this as bearer token to use the API locally or live.

The deployed application has two roles: **Admin** and **User**

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
Local:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/questions`

Deployed:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://trivia-api-jeff.herokuapp.com/questions`

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
Local:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/categories`

Deployed:
`curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://trivia-api-jeff.herokuapp.com/categories`

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
Local:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  http://127.0.0.1:5000/questions
```

Deployed:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  https://trivia-api-jeff.herokuapp.com/questions
```

```
{
    "new_question": 3,
    "success": true
}
```

#### POST /questions (with search)
Local:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"searchTerm": "<search_string>"}' \
  http://127.0.0.1:5000/questions
```

Deployed:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"searchTerm": "<search_string>"}' \
  https://trivia-api-jeff.herokuapp.com/questions
```

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
Local:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"type": "<category_name>"}' \
  http://127.0.0.1:5000/categories
```

Deployed:
```
curl --header "Content-Type: application/json" \
  --request POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"type": "<category_name>"}' \
  https://trivia-api-jeff.herokuapp.com/categories
```

```
{
    "new_category": 6,
    "success": true
}
```

#### DELETE /questions/<question_id>
Local:
```
curl --request DELETE \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://127.0.0.1:5000/questions/<question_id>
```

Deployed:
```
curl --request DELETE \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  https://trivia-api-jeff.herokuapp.com/questions/<question_id>
```

```
{
    "success": true
}
```

#### PATCH /questions/<question_id>
Local:
```
curl --header "Content-Type: application/json" \
  --request PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  http://127.0.0.1:5000/questions/<question_id>
```

Deployed:
```
curl --header "Content-Type: application/json" \
  --request PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  --data '{"question": "What is the meaning of life?","answer": "42","difficulty": 2,"category": 4}' \
  https://trivia-api-jeff.herokuapp.com/questions/<question_id>
```

```
{
    "question": 3,
    "success": true
}
```
