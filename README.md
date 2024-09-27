
# Introduction

The goal of this project is a platform where a user can sign up and create an agency and the staff user can activate, deactivate and update agency(user) details. 

Template is written with django 4.2 and python 3.8 in mind.

![Default Home View](__screenshots/home.png?raw=true "Title")

### Main features

* Staff emenbers can sign up

* Non staff members(agencies) can sign up

* After user sign up admin will have to activate thier account before they create an agency

* Staff can activate and deactivate user/agency accounts

* Staff can edit agency details

* Separated requirements files



# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/toyman640/agencybackend.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements/local.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver