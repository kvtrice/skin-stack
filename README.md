# Welcome to Skin Stack 🧴 

This project is an **API webserver** for a simple Skincare Routine Tracker application named Skin Stack, that helps users track their skincare products and daily skincare routines; helping users take the guesswork out of their beauty regime.

### External Links

- [Github Repository](https://github.com/kvtrice/skin-stack)
- [Development Plan (Linear)](https://linear.app/kats-workspace/join/88596d7e69b639b4a651783417b35e23?s=4)


# Table of Contents

👉 Start here: [Installation Instructions](#installation-instructions-macos)

1. [The problem](#1)
2. [Why should we solve it?](#2)
3. [Chosen database system (and it's drawbacks)](#3)
4. [Key functionalities & benefits of an ORM](#4)
5. [API Documentation](#5)
6. [ERD for the application](#6)
7. [Third party services used](#7)
8. [Project models (in terms of the relationships they have with each other)](#8)
9. [Database relations implemented in this app](#9)
10. [Task allocation & tracking (develolpment plan)](#10)

# Installation Instructions (MacOS)

### Create Python Virtual Environment

1. Open the Terminal to the folder where the project is located and run the following command:

```bash
python3 -m venv .venv
```

2. Activate the virtual environment and open VS Code:
```bash
source .venv/bin/activate
```
```bash
code .
```

### Install Dependencies

1. Open a terminal window and install the project dependencies from the `requirements.txt` file using the following command:
```bash
pip install -r requirements.txt
```

### Create a new postgreSQL database

1. In a Terminal window start the PostgreSQL server with the following command:

```bash
service postgresql start
```

2. Open psql and create a database called 'skincare' with the following commands

```bash
psql postgres
```
```postgresql
create database skincare
```

### Create, Seed and Run the Database
1. Ensure you've exited out of `psql`. Then create the database with the project models use the following command:
```bash
flask db create
```

2. Seed the database with some starting data using the following command:
```bash
flask db seed
```

3. Finally run the database server in order to access the API endpoints, using the following command:
```bash
flask run
```

### Configuration
1. In Insomnia (or chosen tool) I've used port 5000. For example:
`http://127.0.0.1:5000` or `http://localhost:5000`. You can use this port too.

2. This port should then be added as the default port (`FLASK_RUN_PORT`) into your `.flaskenv` file. If you are yet to create your `.flaskenv` file, an example configuratiton can be found at `.flaskenv.sample`:

```python
FLASK_RUN_PORT=5000
# ...
```

3. Ensure your JWT Key and the Database URI are also added to the `.flaskenv`. 

```python
JWT_KEY= # JWT signing key
DB_URI= # Database URI string
```


# Project Documentation ⬇️

## 1. The problem 🙅‍♀️ <div id="1"/>

Millions of people globally have some kind of skincare routine; this can range from a simple daily moisturiser to a complex 10 step regime. But as a skincare routine grows, so too does the number of products you have, and the number of interactions between products that need to be considered. Some products need to be used at night time, others in the morning, some need to be washed of immediately, others kept on, some can't be used in conjunction with certain other products and others need to be used only twice a week. How do you keep track of it all?

## 2. Why should we solve it? 🤔 <div id="2"/>

As someone that's recently embarked on a skincare journey I've felt this pain first hand. It's become increasingly challenging to keep track of which products I should be using, when I should be using them and what order I should be using them in. I've been on the hunt for solutions to help me track my routines but every application I tried is either too costly, has a lot of extra's around mood or food tracking and other aspects I'm not interested in or has poor UI making it frustrating to navigate. It's seemed impossible to find a simple, no-fluff skincare routine tracker that let's me add products in a click and tracks the what, how and when of my daily skincare routines.

And when speaking to people around me, it seems I'm not alone. Many have resorted to just using the notes app in their phone in lieu of a better solution. And as you can imagine it quickly becomes frustrating to manually add and change products or routines across all days of the week, not to mention the lack of product tracking or home screen reminders.

This is where Skin Stack comes in - an intuitive no-frills way to track and maintain your skincare routines without the effort.

## 3. Chosen database system (and it's drawbacks) 🚦 <div id="3"/>

PostgreSQL was chosen as it is a powerful relational database management system. For my project this is an important factor given the many-to-many relationship between Routines and Products (described in the ERD above). Additionally PostgreSQL offered more scalability and extensibility than other options (such as MySQL), as well as having robust data integrity functionality, making future project enhancements and expansions possible with ease.

However it's worth noting that these advantages do come with the trade off of performance. PostgreSQL being so highly exstensible comes at a cost, and as such it's not as lightweight as some of it's competitors. Taking thsi into consideration, having concurrency handled extremely well and certainty about the integrity of my data was worth the trade off.

## 4. Key functionalities & benefits of an ORM 💡 <div id="4"/>

## 5. API Endpoints ☁️ <div id="5"/>

### Endpoint Directory
1. [Register user](#1-register-user)
2. [Login user](#2-login-user)
3. [Get all users (Global - Admin only)](#3-get-all-users)
4. [Get all products (Global - Admin only)](#4-get-all-products)
5. [Get all Routines (Global - Admin only)](#5-get-all-routines)
6. [Create a product](#6-create-a-product)
7. [Update a product](#7-update-a-product)
8. [Delete a product](#8-delete-a-product)
9. [Get user products](#9-get-user-products)
10. [Create a routine](#10-create-a-routine)
11. [Add a product to a routine](#11-add-a-product-to-a-routine)
12. [Delete a product from a routine](#12-delete-a-product-from-a-routine)
13. [Delete a routine](#13-delete-a-routine)
14. [Get user routines](#14-get-user-routines)

### 1. Register user
Allows a user to create an account for the application.

- Endpoint: `/users/register`
- Request Verb: `POST`
- Required data:
  - `first_name`
  - `last_name`
  - `email`
  - `password`
- Expected Response: `201 CREATED` 
  - Return all data *excluding* `password`
- Authentication: None for registering a user. Password is hashed upon registration using Bcrypt.

Example Request:
```JSON
{
	"first_name": "Kat",
	"last_name": "Test",
	"email": "kat@tester.com",
	"password": "password"
}
```

Example Response:

```JSON
{
	"email": "kat@tester.com",
	"first_name": "Kat",
	"id": 1,
	"is_admin": false,
	"last_name": "Test"
}
```
---

### 2. Login user
Allows a registered user to login to the application. 

- Endpoint: `/users/login`
- Request Verb: `POST`
- Required data:
  - `email`
  - `password`
- Expected Response: `200 OK` 
  - Return all data *including* JWT `token` but *excluding* `password`
- Authentication: User is authenticated based on matching email and password. If matching, a JWT token is generated for the user.

Example Request:
```JSON
{
	"email": "admin@admin.com",
	"password": "password"
}
```


Example Response:

```JSON
{
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTc1MjMwMCwianRpIjoiNTkzYzc4MzktMzA4NC00YzNmLWE4NDYtYzBjMmExZGM3Y2JmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzAxNzUyMzAwLCJleHAiOjE3MDE3NTU5MDAsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwiZmlyc3RfbmFtZSI6IkthdCJ9.cAZwDQRKRG9aRgpTMMIjusBkvvz8eQV2As_CnXBzye4",
	"user": {
		"email": "admin@admin.com",
		"first_name": "Kat",
		"id": 1,
		"is_admin": true,
		"last_name": "Admin"
	}
}
```
---
### 3. Get all users
Allows an administrator to get a list of all registered users in the application

- Endpoint: `/users`
- Request Verb: `GET`
- Required data: None
- Expected Response: `200 OK` 
  - Return all user data *excluding* `password`
- Authentication: JWT token must be valid *and* `is_admin` = true (handled by `admin_required()` function)


Example Response:

```JSON
[
	{
		"email": "admin@admin.com",
		"first_name": "Kat",
		"id": 1,
		"is_admin": true,
		"last_name": "Admin"
	},
	{
		"email": "test@gmail.com",
		"first_name": "Testa",
		"id": 2,
		"is_admin": false,
		"last_name": "Testerson"
	}
]
```
---
### 4. Get all products
Allows an administrator to get a list of all products in the application (from any user)

- Endpoint: `/products`
- Request Verb: `GET`
- Required data: None
- Expected Response: `200 OK` 
  - Return all product data along with the associated user data *excluding* `password` and `is_admin`
- Authentication: JWT token must be valid *and* `is_admin` = true (handled by `admin_required()` function)


Example Response:

```JSON
[
	{
		"brand": "CeraVe",
		"id": 1,
		"name": "Daily Moisturiser",
		"notes": "Use both AM & PM. Contains Hylauronic Acid.",
		"user": {
			"email": "admin@admin.com",
			"first_name": "Kat",
			"id": 1,
			"last_name": "Admin"
		}
	}
]
```
---
### 5. Get all routines
Allows an administrator to get a list of all routines in the application (from any user), along with the associated products (if any) within the routine/(s).

- Endpoint: `/routines`
- Request Verb: `GET`
- Required data: None
- Expected Response: `200 OK` 
  - Returns all routine data along with the associated product data *excluding* `routine_id` and `product_id` from `routine_products` as these are already returned as part of the routine and product schema's resepctively (would be duplicate values). Also excluding additional user data save for `user_id`
- Authentication: JWT token must be valid *and* `is_admin` = true (handled by `admin_required()` function)

Example Response:

```JSON
[
	{
		"created_at": "2023-12-05",
		"day_of_week": "Monday",
		"id": 1,
    "time_of_day": "AM",
		"user_id": 1,
		"routine_products": [
			{
				"id": 1,
				"product": {
					"brand": "CeraVe",
					"id": 1,
					"name": "Daily Moisturiser",
					"notes": "Use both AM & PM. Contains Hylauronic Acid."
				}
			},
			{
				"id": 2,
				"product": {
					"brand": "The Ordinary",
					"id": 2,
					"name": "Niacinimide",
					"notes": "Very drying for my skin, I prefer to use it only once a day max. Apply before heavy creams."
				}
			}
		]
	},
  {
    "created_at": "2023-12-05",
    "day_of_week": "Sunday",
    "id": 2,
    "time_of_day": "PM",
    "user_id": 2,
    "routine_products": []
  },
]
```
---
### 6. Create a product
Allows a registered user to create a new product for themselves.

- Endpoint: `/products`
- Request Verb: `POST`
- Required data:
  - `name`
  - `brand`
  - `notes`
- Expected Response: `201 CREATED` 
  - Return all product data *excluding* associated user information
- Authentication: JWT token must be valid.

Example Request:
```JSON
{
	"name": "Lactic Acid 2%",
	"brand": "The Ordinary",
	"notes": "Use every other day for my skin, otherwise it's too drying"
}
```

Example Response:

```JSON
{
	"brand": "The Ordinary",
	"id": 7,
	"name": "Lactic Acid 2%",
	"notes": "Use every other day for my skin, otherwise it's too drying"
}
```
---
### 7. Update a product
Allows a registered user to update an existing product. Standard users are only able to update their own products whilst admins are able to update any product in the database.

- Endpoint: `/products/<int:product_id>`
- Request Verb: `PUT`
- Required data:
  - `name` or
  - `brand` or
  - `notes`
  - Any combination of the fields can be optionally updated 

- Expected Response: `200 OK` 
  - Return all product data *excluding* associated user information
- Authentication: JWT token must be valid. Checks that the user making the request matches the user_id associated with the product OR if the user is an admin.

Example Request:
```JSON
{
  "notes": "This is an updated note"
}
```

Example Response:

```JSON
{
	"brand": "The Ordinary",
	"id": 7,
	"name": "Lactic Acid 2%",
	"notes": "This is an updated note"
}
```
---
### 8. Delete a product
Allows a registered user to delete an existing product. Standard users are only able to delete their own products whilst admins are able to delete any product in the database.

- Endpoint: `/products/<int:product_id>`
- Request Verb: `DELETE`
- Required data: None
- Expected Response: `200 OK` 
  - Return confirmation of successful delete operation
- Authentication: JWT token must be valid. Checks that the user making the request matches the user_id associated with the product OR if the user is an admin.

Example Response:

```JSON
{
	"Message": "Product has been successfully deleted"
}
```
---
### 9. Get user products
Allows a registered user to get a list of their products. Standard users are only able to access a list of products associated with their own user_id. Admins are able to get a list of products associated with any user_id. In both cases, the list of products is scoped to that of the provided user_id.

- Endpoint: `/products/<int:user_id>`
- Request Verb: `GET`
- Required data: None
- Expected Response: `200 OK` 
  - Return all products along with the product data *excluding* associated user information
- Authentication: JWT token must be valid. Checks that the user making the request matches the user_id provided in the request OR if the user is an admin.

Example Response:

```JSON
[
	{
		"brand": "CeraVe",
		"id": 1,
		"name": "Daily Moisturiser",
		"notes": "Use both AM & PM. Contains Hylauronic Acid."
	},
	{
		"brand": "The Ordinary",
		"id": 2,
		"name": "Niacinimide",
		"notes": "Very drying for my skin, I prefer to use it only once a day max. Apply before heavy creams."
	}
]
```
---
### 10. Create a routine
Allows a registered user to create a new skincare routine for themselves.

- Endpoint: `/routines`
- Request Verb: `POST`
- Required data:
  - `day_of_week`
    - Acceptable values: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`
  - `time_of_day`
    - Acceptable values: `AM`, `PM`
- Expected Response: `201 CREATED` 
  - Return all routine data.
- Authentication: JWT token must be valid.

Example Request:
```JSON
{
	"day_of_week": "Sunday",
	"time_of_day": "PM"
}
```

Example Response:

```JSON
{
	"created_at": "2023-12-05",
	"day_of_week": "Sunday",
	"id": 6,
	"time_of_day": "PM"
}
```
---
### 11. Add a product to a routine
Allows a registered user to add an existing product to an existing routine. Users are only able to complete this operation on their own products and their own routine unless they are an admin.

- Endpoint: `/routines/<int:routine_id>/products/<int:product_id>`
- Request Verb: `POST`
- Required data: None; Both the routine_id and product_id are provided in the request, so no JSON body is required.
- Expected Response: `200 OK` 
  - Return confirmation of successful operation
- Authentication: JWT token must be valid. Both the user_id of the requested routine and the user_id of the requested product must match the authenticated user OR the user must be an admin.

Example Response:

```JSON
{
	"Message": "Product has been successfully added to this routine."
}
```
---
### 12. Delete a product from a routine
Allows a registered user to delete an existing product from an existing routine. Users are only able to complete this operation on their own products and their own routines unless they are an admin.

- Endpoint: `/routines/<int:routine_id>/products/<int:product_id>`
- Request Verb: `DELETE`
- Required data: None; Both the routine_id and product_id are provided in the request, so no JSON body is required.
- Expected Response: `200 OK` 
  - Return confirmation of successful operation
- Authentication: JWT token must be valid. Both the user_id of the requested routine and the user_id of the requested product must match the authenticated user OR the user must be an admin.

Example Response:

```JSON
{
	"Message": "Product has been successfully deleted from this routine."
}
```
---
### 13. Delete a routine
Allows a registered user to delete an existing routine. Standard users are only able to delete their own routines whilst admins are able to delete any routine in the database (from any user). Deleting a routine does not delete any products within it, it only deletes the routine_product relationship.

- Endpoint: `/routines/<int:routine_id>`
- Request Verb: `DELETE`
- Required data: None
- Expected Response: `200 OK` 
  - Return confirmation of successful delete operation
- Authentication: JWT token must be valid. Checks that the user making the request matches the user_id associated with the routine OR if the user is an admin.

Example Response:

```JSON
{
	"Message": "Routine has been successfully deleted. Any products have been dissasociated but not deleted."
}
```
---
### 14. Get user routines
Allows a registered user to get a list of their routines along with the associated products. Standard users are only able to access a list of routines associated with their own user_id. Admins are able to get a list of routines associated with any user_id. In both cases, the list of routines is scoped to that of the provided user_id in the request.

- Endpoint: `/routines/<int:user_id>`
- Request Verb: `GET`
- Required data: None
- Expected Response: `200 OK` 
  - Return all routines along with the product data *excluding* associated user information
- Authentication: JWT token must be valid. Checks that the user making the request matches the user_id provided in the request OR if the user is an admin.

Example Response:

```JSON
[
	{
		"created_at": "2023-12-05",
		"day_of_week": "Monday",
		"id": 2,
    "time_of_day": "PM",
		"routine_products": [
			{
				"product": {
					"brand": "The Ordinary",
					"id": 2,
					"name": "Niacinimide",
					"notes": "Very drying for my skin, I prefer to use it only once a day max. Apply before heavy creams."
				}
			},
			{
				"product": {
					"brand": "The Ordinary",
					"id": 6,
					"name": "Lactic Acid",
					"notes": "Use every other day for my skin, otherwise it's too drying"
				}
			}
		]
	},
	{
		"created_at": "2023-12-05",
		"day_of_week": "Sunday",
		"id": 5,
		"time_of_day": "AM",
		"routine_products": []
	},
	{
		"created_at": "2023-12-05",
		"day_of_week": "Sunday",
		"id": 6,
		"time_of_day": "PM",
		"routine_products": [],
	}
]
```

## 6. ERD 📚 <div id="6"/>

![ERD](docs/erd/skin_stack_erd.jpg)

### Key points:

- A user can have many routines
- A user can add many products
- Products can be added and not necessarily be in a routine
- Routines can technically be empty
- The workflow: empty routines are created and then products are later added to them
- Either new or existing products can be added to routines
  - (Will check if product exists first and if not, create a new one)
- Routines and products are scoped to a user, so they have full control over everything (Create, update, delete, get). There is no shared database across all users

## 7. Third party services used 🤝 <div id="7"/>

Throughout the course of this project, multiple third party services have been utillised to create this application. Some of the key ones include:

### SQL Alchemy

### Marshmallow

### Bcrypt

### JWT Manager

## 8. Project models (in terms of the relationships they have with each other) 🧱 <div id="8"/>

### User model

### Product model

### Routine model

### RoutineProduct model

## 9. Database relations implemented in this app 👫 <div id="9"/>

## 10. Task allocation & tracking (development plan) 💻 <div id="10"/>

[Link to Linear Board](https://linear.app/kats-workspace/join/88596d7e69b639b4a651783417b35e23?s=4)

Tasks were tracked using Linear.

### Linear Board

![Image 1.0](/docs/development_plan/1.0.jpg)
![Image 1.1](/docs/development_plan/1.1.jpg)
![Image 1.2](/docs/development_plan/1.2.jpg)
![Image 1.3](/docs/development_plan/1.3.jpg)
![Image 1.4](/docs/development_plan/1.4.jpg)
![Image 1.5](/docs/development_plan/1.5.jpg)
![Image 2.0](/docs/development_plan/2.0.jpg)
![Image 2.1](/docs/development_plan/2.1.jpg)
![Image 2.2](/docs/development_plan/2.2.jpg)
![Image 3.0](/docs/development_plan/3.0.jpg)
![Image 3.1](/docs/development_plan/3.1.jpg)
![Image 3.2](/docs/development_plan/3.2.jpg)
![Image 3.3](/docs/development_plan/3.3.jpg)
![Image 4.0](/docs/development_plan/4.0.jpg)
![Image 4.1](/docs/development_plan/4.1.jpg)
![Image 4.2](/docs/development_plan/4.2.jpg)
