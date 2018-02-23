import base64
import urllib

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string


class InvalidUserHashException(Exception):
	pass


class UtilityManager(object):
	
	@staticmethod
	def calculate_user_hash(user_dtls):
		return base64.b32encode("{}-{}".format(user_dtls.id, user_dtls.username))
	
	@staticmethod
	def get_user_from_hash(user_hash):
		user_dtls = base64.b32decode(user_hash)
		splitted_user_dtls = user_dtls.split("-")
		
		if len(splitted_user_dtls) != 2:
			raise InvalidUserHashException("Invalid user hash: {}".format(user_hash))
		
		return splitted_user_dtls
	
	@staticmethod
	def send_user_account_activation_email(target_url, user_dtls, sender, auth_user, auth_password):
		user_hash = UtilityManager.calculate_user_hash(user_dtls)
		user_token = PasswordResetTokenGenerator().make_token(user_dtls)
		
		query_string = urllib.urlencode({"user": user_hash, "token": user_token})
		url_with_query_str = "{}?{}".format(target_url, query_string)
		
		template_name = "account-activate-email.txt"
		context = {
			"username": user_dtls.username,
			"target_url": url_with_query_str
		}
		
		subject = "Account Activation email"
		receivers = [user_dtls.email]
		message_body = render_to_string(template_name, context)
		
		return UtilityManager.send_email(subject, message_body, sender, receivers, auth_user, auth_password)
	
	@staticmethod
	def reset_user_account_password_email(target_url, user_dtls, sender, auth_user, auth_password):
		user_hash = UtilityManager.calculate_user_hash(user_dtls)
		user_token = PasswordResetTokenGenerator().make_token(user_dtls)
		
		query_string = urllib.urlencode({"user": user_hash, "token": user_token})
		url_with_query_str = "{}?{}".format(target_url, query_string)
		
		template_name = "password-reset-email.txt"
		context = {
			"username": user_dtls.username,
			"target_url": url_with_query_str
		}
		
		subject = "Password Reset Email"
		receivers = [user_dtls.email]
		message_body = render_to_string(template_name, context)
		
		return UtilityManager.send_email(subject, message_body, sender, receivers, auth_user, auth_password)
	
	
	@staticmethod
	def send_email(subject, body, sender, receivers, auth_user, auth_password):
		send_mail(
			subject, body, sender, receivers, 
			fail_silently=False, auth_user=auth_user, auth_password=auth_password
		)
