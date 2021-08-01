# Capstone Project - Motivation for project

This is the latest project of the Fullstack nanograduate, an API that is based on the management of a casting agency. Based on roles, and functionalities, which through Auth0 secures all the information traffic. I feel very excited to be able to finish it.

Url: `% https://nherreracapstone.herokuapp.com/ `

### Starts

0. Requires Python 3.5 or higher.

1. Clone the  repository: https://github.com/natherrera/UDACITYCapstone.git 

2. Install the requirements (using a virtualenv is encouraged).

   `% pip install -r requirements.txt`

3. Start a postgresql database.  I'm sure my audience of one Sir/Madam Udacity Reviewer can manage.

   `% createdb capstone`

4. Edit setup.sh to set DATABASE_URL to your database url.

5. Source the setup script.

   `% source setup.sh`

7. Run the flask app.

   `% flask run`

#### roles

Exists three roles, in order of hierarchy:

1. Executive Producer
2. Casting Director
3. Casting Assistant

# JWTs

ASSISTANT = '<assistant jwt goes here>'
DIRECTOR = '<director jwt goes here>'
PRODUCER = '<producer jwt goes here>'
```

# API and Roles permissions

Method | URL | Authorization
------ | --- | -------------
GET    | /actors | All Roles
GET    | /actors/:id | All Roles
GET    | /movies | All Roles
GET    | /movie/:id | All Roles
POST   | /actor | Director
POST   | /movie | Producer/Director
PATCH  | /actor/:id | Director
PATCH  | /movie/:id | Director
DELETE | /actor/:id | Director
DELETE | /movie/:id | Producer/Director

#API-Reference

## Actors

#### Actor Attributes
- **id** `integer`
- **name** `string`
- **gender** `string`

#### GET ACTORS **/actors**

- Description: List all of actors

- Authorization: **All roles**

- URL Parameters: None

- JSON Payload: No Required

- Curl: 

    ```
    % curl -H $AUTHORIZED_HEADER 'http://127.0.0.1:5000/actors'
    ```
- Response:

    ```
   {
      "actors": [
          {
              "gender": "female",
              "id": 1,
              "name": "Natalia"
          },
          {
              "gender": "Male",
              "id": 2,
              "name": "Quentin"
          }
      ],
      "status_code": 200,
      "success": true
    }
    ```

#### POST ACTORS **/actors/:id**

- Description: Create new actor

- Authorization Level: **Executive Producer**

- URL Parameters: id <int>

- JSON Payload: **Required**

- Curl:  

```
    % curl \
    -X POST \
    -H $AUTHORIZED_HEADER \
    -H 'Content-Type:application/json' \
    -d '{"name": "Pamela" "gender":"female"}' \
    'http://127.0.0.1:5000/actors'
```

- Response:

    ```
    {
      "actor": {
          "gender": "female",
          "id": 38,
          "name": "Pamela"
      },
      "status_code": 200,
      "success": true
    } 
    ```

#### PATCH ACTOR **/actors/:id**

- Description: Update an actor

- Authorization Level: **Executive Producer**

- URL Parameters: id <int>

- JSON: **Required**

- Curl:

    ```
    % curl \
    -X PATCH \
    -H $AUTHORIZED_HEADER \
    -H 'Content-Type:application/json'
    -d '{"name": "Jason Lee II"}' \
    'http://127.0.0.1:5000/actors/2'
    ```
- Response:
    ```
    {
      "actor_updated": {
          "gender": "female",
          "id": 2,
          "name": "Natalia"
      },
      "status_code": 200,
      "success": true
    }

    ```
#### DELETE ACTOR **/actors/:id**

- Description: Delete an actor

- Authorization Level: **Executive Producer**

- URL Parameters: id <int>

- JSON: No required

- Curl:

```
% curl \
-X DELETE \
-H $AUTHORIZED_HEADER \
'http://127.0.0.1:5000/actors/2'
```
- Response:
```
  {
      "deleted_actor_id": 2,
      "status_code": 200,
      "success": true
  }
```

## Movies

#### Movie Attributes

- **id** `integer`
- **title** `string`
- **release_date** `date`

#### GET MOVIES **/movies**

- Description: List all of movies

- Authorization: **All roles**

- URL Parameters: None

- JSON Payload: **NO Required**

- Curl: 

    ```
    % curl \
    -H $AUTHORIZED_HEADER \
    'http://127.0.0.1:5000/movies'
    ```
- Response:

    ```
    {
      "movies": [
          {
              "id": 1,
              "release_date": "2021-11-11 00:00:00",
              "title": "Cobra"
          },
          {
              "id": 2,
              "release_date": "2021-11-11 00:00:00",
              "title": "The Internet"
          }
      ],
      "status_code": 200,
      "success": true
    }

    ```

#### POST MOVIES **/movies**

- Description: Create new movie

- Authorization Level: **Executive Producer**

- URL Parameters: None

- JSON Payload: **Required**

- Curl:  
    ```
    % curl \
    -X POST \
    -H $AUTHORIZED_HEADER \
    -H 'Content-Type:application/json' \
    -d '{"title": "Twin Peaks", "release_date": "2021-11-11 00:00:00"}' \
    'http://127.0.0.1:5000/movies'
    ```
    Response
    ```
    {
        "movie": {
            "id": 2,
            "release_date": "2021-11-11 00:00:00",
            "title": "Twin Peaks"
        },
        "status_code": 200,
        "success": true
    }
    ```


#### PATCH MOVIE **/movies/:id**

- Description: Update an movie

- Authorization Level: **Executive Producer**

- URL Parameters: id <int>

- JSON: **Required**

- Curl:

    ```
    % curl \
    -X PATCH \
    -H $AUTHORIZED_HEADER \
    -H 'Content-Type:application/json'
    -d '{"name": "Mask"}' \
    'http://127.0.0.1:5000/movies/1'
    ```
- Response:
    ```
    {
      "movie_updated": {
          "title": "Mask",
          "id": 1,
          "release_date": "2021-11-11 00:00:00"
      },
      "status_code": 200,
      "success": true
    }

    ```

#### DELETE ACTOR **/actors/:id**

- Description: Delete an actor

- Authorization Level: **Executive Producer**

- URL Parameters: id <int>

- JSON: No required

- Curl:

```
% curl \
-X DELETE \
-H $AUTHORIZED_HEADER \
'http://127.0.0.1:5000/actor/1'
```
- Response:
```
{
    "deleted_movie_id": 1,
    "status_code": 200,
    "success": true
}
```