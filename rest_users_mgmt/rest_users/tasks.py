import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_users_mgmt import celery_app as app
from rest_users.utils import UtilityManager

USER_MODEL = get_user_model()
LOGGER = logging.getLogger("workers")


@app.task
def send_account_activation_email(user_id, target_url, task_id=None):
	try:
		user_instance = USER_MODEL.objects.get(pk=user_id)
	
	except USER_MODEL.DoesNotExist:
		LOGGER.error("Task: %s ==> user with %s: {} doesnot exists", task_id, user_id)
	
	else:
		LOGGER.debug("Task: %s ==> Sending account activation email", task_id)
		UtilityManager.send_user_account_activation_email(
			target_url, user_instance, 
			settings.EMAIL_HOST_USER, 
			settings.EMAIL_HOST_USER, 
			settings.EMAIL_HOST_PASSWORD
		)
		LOGGER.debug("Task: %s ==> Account activation email sent", task_id)

@app.task
def send_password_reset_email(user_id, target_url, task_id=None):
	try:
		user_instance = USER_MODEL.objects.get(pk=user_id)
	
	except USER_MODEL.DoesNotExist:
		LOGGER.error("Task: %s ==> user with %s: {} doesnot exists", task_id, user_id)
	
	else:
		LOGGER.debug("Task: %s ==> Sending Account reset email", task_id)
		UtilityManager.reset_user_account_password_email(
			target_url, user_instance, 
			settings.EMAIL_HOST_USER, 
			settings.EMAIL_HOST_USER, 
			settings.EMAIL_HOST_PASSWORD
		)
		LOGGER.debug("Task: %s ==> Account reset email sent", task_id)
