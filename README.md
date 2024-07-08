# Quizzerz

![Quizzerz Logo](static/images/Quizzerz%20logo.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Introduction](#introduction)
- [License](#license)


## Introduction

Quizzerz is an interactive quiz application that comprizes of four categories of questions, i.e Geography, Science, Mathematics and English, just a fun way of testing your knowledge 😉.

## Features

- User authentication and authorization.
- User category questions
- Checking result history with option details
- Admin panel for adding new questions, deleting users that might be harmful 

## Installation

The project is now yet to be deployed, for the mean time in order to access the project

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Grandkojo/Quizzerz.git
    ```

2. **Set up the web server:**
    - The project was built with Flask.
    - Create a new virtual environment and run the `requirements.txt` file to get the required modules
    ```bash
    pip install -r requirements.txt
    ```
    - Set up a Supabase account, to connect to the database
    - Create a .env file that has the database password and the username: kindly follow the naming in the app.py file

3. **Important**
    - The landing/home page : ```localhost:5000/```
    - The admin landing page: ```localhost:5000/admin/```
    - API routes: ```localhost:5000/api/v1/**```

You're good to go 🥳.

## Usage

1. **User registration and / or signup**
    - Users can signup or login to the application to access the quiz questions.

2. **Choose category specific questions**
    - Users are presented with four category of questions to answer or choose from.

3. **View results history**
    - Users can also check the results of all their previous quizzes they took according to the most recent with also also answers they chose with their correspondin correctness.


## Project Structure

QUIZZERZ/<br>
|-- api/<br>
|&emsp; |--v1/<br>
|&emsp; |--views/<br>
|-- init_data/<br>
|-- landing_page/<br>
|-- myenv/<br>
|-- static/<br>
|-- templates/<br>
|-- .env<br>
|-- .gitignore<br>
|-- app.py<br>
|-- LICENSE<br>
|-- README.md<br>
|-- requirements.txt<br>


## Technologies Used

- Flask (framework).
- Supabase (Postgresql database).
- Bootstrap: Front-end framework for responsive web design.
- Javascript: For making the app dynamic.

## License

This project is licensed under the [MIT License](LICENSE).


- This is my ALX SWE webstack portfolio project. Thanks @[ALX](https://www.alxafrica.com/)
