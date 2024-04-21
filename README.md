# Job Portal Application

This is an Jobportal website created using Django web framework with sqlite3 as a database.

## Features

* User registration and authentication
* edit/update profile
* Job provider can Post new job openings
* Job provider can see the list of jobseekers who has applied for the job
* Job provider can see and download the jobseeker’s resume
* Accept/reject applicants(email will send to the candidate)
* Recruiters can post company images to website
* Reset/change password
* Jobseeker can Search for jobs
* Apply Online for desire job
* View list of applied jobs
* View application status (accepted/rejected)
* Admin can approve, reject the registered recruiter(email will send to recruiters)


## Technology Stack

* Frontend: HTML/CSS, JavaScript, Bootstrap
* Backend: Python
* Web Framework: Django
* Database: Sqlite3


## Getting Started

1. Create a virtual environment and activate it

```
virtualenv venv
python -m virtualenv venv
venv\Scripts\activate

2. Install dependencies

pip install django
pip install django-filter
pip install django-widget-tweaks

INSTALLED_APPS = [
    ...
    
    'django_filters',
    'widget_tweaks',
]

3. using the default sqlite3 database and add the database credentials to settings.py


4. Run database migrations


python manage.py makemigrations
python manage.py migrate


5. Start the development server


python manage.py runserver


6. Open the website in your browser at http://localhost:8000


### add email and password for the the email sending


EMAIL_USE_TLS=True

EMAIL_HOST='smtp.gmail.com'

EMAIL_PORT=587

EMAIL_HOST_USER=''#add mail here

EMAIL_HOST_PASSWORD='' # add password here   

###email used as the authentication backend for login  ( username and email for login [backends.py] )

AUTHENTICATION_BACKENDS=['jobportalapp.backends.EmailBackend']

### django filter is used for searching( filter.py)
###  profile image setting in nav bar ( context_processors.py)
