# Videoflix (Backend)

Table of Contents
=================

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Upload a video for the website to work](#how-to-upload-new-videos)
* [Register a user on the website](#register-a-user-on-the-website)
* [API Documentation](#api-documentation)
* [Features](#features)

## Introduction

Videoflix is a full stack video streaming platform for demonstration purposes. The platform allows superusers to upload videos and 'normal' users to register (including email activation) and watch the catgorized videos.

## Prerequisites

* Python
* Redis
* FFmpeg
* PostgreSQL

## Installation

This is a backend to host on Linux (like most backends), so if you are not already using Linux and want to test this project on Windows, you have to use a Linux emulator of your choice.

### On Linux

1. Install the latest Python, Redis, FFmpeg and PostgreSQL version.
2. Clone the repository.
3. Navigate into the cloned folder and activate the environment.
```
python3 -m venv env
source env/bin/activate
```
4. Install the required packages using pip.
```
pip install -r requirements.txt
```

## Getting Started

### Start postgresql

After you installed postgres, please make sure, the service is running:
```
service postgresql start
```
Connect to your postgres:
```
sudo -u postgres psql
```
Then you can setup your database. Please enter your Linux username and create your own password in the following commands.

```
CREATE DATABASE videoflix;
CREATE ROLE your_linux_username WITH PASSWORD 'your_postgres_password';
ALTER ROLE your_linux_username WITH LOGIN;
ALTER ROLE your_linux_username SET client_encoding TO 'utf8';
ALTER ROLE your_linux_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_linux_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE videoflix TO your_linux_username;
ALTER USER your_linux_username WITH SUPERUSER;
\q
```

It is also important to add these two credentials to the .env file of this project.

After creating the database with it's user, do migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Start the rest

Start the script for running the backend localhost, redis and celery services using the given script:
```
./start_services.sh
```

## Upload a video for the website to work

1. Create a superuser.
```
python manage.py createsuperuser
```
2. Login to the [admin interface](http://127.0.0.1:8000/videoflix/admin/video_app/video/) for uploading videos.
3. Fill in title, description, category, upload a video file and a thumbnail picture.

This process will convert the video to different resolutions as a background process in the database.
You can then register a user on the frontend, login and watch the videos on the hosted frontend.

## Register a user on the website

Host the [frontend](https://github.com/Pe3et/Videoflix_frontend) part locally. 

In order to receive a required registration email to be able to test the logged in and password reset functionality, you first need to add existing email credentials in order to receive emails from that added account.
You can do this by filling out the three lines in the .env file.

## API Documentation

When you hosted the project, you can see the documentation here: 
http://127.0.0.1:8000/videoflix/schema/swagger-ui/

If you want to check the test coverage, run the following commands:
```
coverage run manage.py test
```
```
coverage report
```

## Mentionable Features

* Reset Password via email
* Changing resolutions in video player 