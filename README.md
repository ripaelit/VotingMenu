# Vote Menu - Test Project by Teofil Kobylarz

## 🙏 Appreciation

Thanks for those reviewing my code.

Understanding is noble deed which requires patience.

And so I tried to be as specific as possible in this guide documentation so that those reviewing my code will find it easy to check out my work. But you might have some questions still.

In that case or if you have some suggestions for me, you can drop me a message here - [ripaelit1111@gmail.com](mailto:ripaelit1111@gmail.com)

> Alone we can do so little; together we can do so much.

## Purpose

This is a DRF(Django REST Framework) project by Teofil Kobylarz for demonstration.

Upload menu for restaurant

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Deployment

The following details how to deploy this application.

### Local

- Follow the guide - [cookiecutter-django Getting up and running locally](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html).

- Create .env file in your project and set the environment variables below:
  DATABASE_URL=postgres://postgres:debug@127.0.0.1:5432/test_project
  USE_DOCKER=False
  CELERY_BROKER_URL=redis://localhost:6379/0

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## Basic Commands (After Deployment)

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## API Documentation

### 1. Interactive Doc ....

API consumers can find interactive API documentation if he opens the URL of each API endpoint in browser.

You can start by browsing the following URLs.

https://localhost:8000/api/users/
https://localhost:8000/api/users/allen (you can replace the number with actual username)
https://localhost:8000/api/restaurants/
https://localhost:8000/api/restaurants/1 (you can replace the number with actual ID)
https://localhost:8000/api/menus/
https://localhost:8000/api/menus/1 (you can replace the number with actual ID)
https://localhost:8000/api/votes/
https://localhost:8000/api/votes/1 (you can replace the number with actual ID)
https://localhost:8000/api/votes/vote_menu

### 2. Postman File

VoteMenuProject.postman_collection.json

## Approach to the Project

### Requirement Analysis

In real project, I'd confirm the requirement before start coding.

### Coding Principles

- Fat Model Principle
- Test driven development (TDD)
- Small App Principle
  [When in Doubt, Keep Apps Small]
  Don’t worry too hard about getting app design perfect. It’s an art, not a science. Sometimes you have to rewrite them or break them up. That’s okay. Try and keep your apps small. Remember, it’s better to have many small apps than to have a few giant apps.

### (Django App Structure) Dependency

users <-- menus <-- votes

| App   | Models           |
| ----- | ---------------- |
| users | User             |
| menus | Restaurant, Menu |
| votes | Vote             |

### Model Structure

![model diagram](images/model_diagram.png)

### About Server Availability

The intention is to use Kubernetes. If the cloud server is Azure, we can use AKS and ACS.
And switching to microservices architecture is recommended to develop a server considering scalability and availability.

## Results

![Alt text](images/admin_page_login.png)
![Alt text](images/admin_page-user.png)
![Alt text](images/admin_page-restaurant.png)
![Alt text](images/admin_page-menu.png)
![Alt text](images/admin_page-vote.png)
![Alt text](images/api-user.png)
![Alt text](images/api-restaurant.png)
![Alt text](images/api-menu.png)
![Alt text](images/api-vote.png)
