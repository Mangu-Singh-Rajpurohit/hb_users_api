User Management Application:-
=============================

It allows for the user sign-in, sign-up, login, logout, change password and forget password features.

It uses django + django-rest framework as backend and angular 1 as front-end framework.
It also uses RabbitMQ as message broker.

Rest API can used with application or it can be used standalone by using api token.
This application has two views which will be shown only to logged in users.
 1) landing (which shows api token to user)
 2) change password

Other views are exposed to everyone.

Rest-endpoints:-
================
Following are the rest-endpoints that this application uses

users/signup/
users/signup/activate/
users/heartbeat/
users/logout/
users/session/
users/changepassword/
users/resetpassword/
users/sendemail/
users/validate_reset_token/
users/token/

Running the project:-
============
You can either run project either in terminal or in the docker or can be configured with nginx + uWSGI servers
1) 	Running docker

	Install docker-ce
	run following command docker pull msrajpurohit/rest_users

	run docker run -p 8000:8000 rest_user

2)	Running in the terminal

	Open Terminal:- (Say it terminal1)
	git clone https://github.com/Mangu-Singh-Rajpurohit/hb_users_api.git
	install virtualenv
	activate it
	cd to hb_users_api/rest_users_mgmt
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py runserver

	Open another terminal(say it terminal2)
	run: celery -A rest_users_mgmt worker -l info

Now try to access application from the browser at <your-ip>:8000


TODOs :-
========
Due to time-limit constraints following things couldn't be achieved :-

1)	Using bootstrap to make UI more sophisticated
2)	In docker, use docker-compose to manage rabbitmq and django seperately.
3)	User supervisor to manage application
