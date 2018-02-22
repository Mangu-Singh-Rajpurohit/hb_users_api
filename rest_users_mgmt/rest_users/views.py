import logging

from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.db import transaction
from django.http.response import HttpResponseRedirect

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import NotAuthenticated, NotFound, ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from rest_users.serializers import UserSignUpSerializer, UserPrimaryDtlsSerializer, \
				UserAuthSerializer, UserTokenSerializer
from rest_users.utils import UtilityManager


LOGGER = logging.getLogger("root")
USER_MODEL = get_user_model()


class UserSignupViewSet(CreateModelMixin, GenericViewSet):
	serializer_class = UserSignUpSerializer
	authentication_classes = ()

	def _get_param(self, request, param_name):
		if param_name in request.GET:
			return request.GET[param_name]
		elif param_name in request.POST:
			return request.POST[param_name]
		elif param_name in request.data:
			return request.data[param_name]
			
		return None

	def create(self, request, *args, **kwargs):
		LOGGER.debug("Received request for creating user")
		with transaction.atomic():
			serializer = self.get_serializer_class()(data=request.data)
			serializer.is_valid(raise_exception=True)
			user_instance = serializer.save()
			
			password = request.data["password"]
			user_instance.set_password(password)
			user_instance.is_active = False
			user_instance.save()
		
			#create token for newly created user
			LOGGER.debug("creating token for user")
			
			user_token = Token(user=user_instance)
			user_token.save()
			
			LOGGER.debug("Created token for user")
		
		# Send email to user's email address asynchronously
		UtilityManager.send_user_account_activation_email(request, user_instance, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
		
		user_dtls_serializer = UserPrimaryDtlsSerializer(instance=user_instance)
		LOGGER.info("User: %s created successfully", user_instance.username)
		
		return Response(user_dtls_serializer.data, status=HTTP_201_CREATED)

	@list_route(methods=["GET", "POST", "PUT"])
	def activate(self, request, *args, **kwargs):
		user_token = self._get_param(request, "token")
		user_hash = self._get_param(request, "user")
		
		if not user_token or not user_hash:
			LOGGER.debug("Missing user_token/user_hash for user activation request")
			return HttpResponseRedirect("/templates/activation-failed")
		
		user_id, username = UtilityManager.get_user_from_hash(user_hash)
		try:
			user_instance = USER_MODEL.objects.get(pk=user_id, username=username)
		
		except USER_MODEL.DoesNotExist:
			LOGGER.debug("User with id: {} and name: {} not found".format(user_id, username))
			return HttpResponseRedirect("/templates/activation-failed")
		
		token_gen = PasswordResetTokenGenerator()
		if not token_gen.check_token(user_instance, user_token):
			LOGGER.debug("Token of user with id: {} and name: {} has become invalid".format(user_id, username))
			return HttpResponseRedirect("/templates/activation-failed")
			
		user_instance.is_active = True
		user_instance.save()
		
		try:
			login(request, user_instance)
		except Exception as e:
			LOGGER.error("An error have occured, while performing login of activated account")
			LOGGER.exception(e)
		
		return HttpResponseRedirect("/templates/activation-success")
		

#	Contains method for obtaining session for api usage in web-app.
class UserAuthViewSet(GenericViewSet):
	authentication_classes = ()
	serializer_class = UserAuthSerializer
		
	@list_route(methods=["POST"])
	def session(self, request, *args, **kwargs):
		LOGGER.debug("Received received for authentication from web app")
		
		serializer = self.get_serializer_class()(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		username = request.data["username"]
		password = request.data["password"]
	
		user = authenticate(username=username, password=password)
		if not user:
			LOGGER.error("Authentication failed for username: %s, password: %s", username, password)
			raise NotAuthenticated(detail="Invalid username/password")

		login(request, user)
		LOGGER.debug("Authentication successful for username: %s", username)
		
		return Response({"status": "success"})
	
	@list_route(methods=["GET", "POST"])
	def logout(self, request, *args, **kwargs):
		LOGGER.debug("Received received for logout from web app")
		try:
			logout(request)
			LOGGER.debug("User: %s logged out successfully", request.user.username)
		
		except Exception as e:
			LOGGER.error("An error have occured, while logging out user: %s", request.user.username)
			LOGGER.exception(e)
		
		return HttpResponseRedirect(redirect_to='/')


	@list_route(methods=["GET"], 
		authentication_classes=(TokenAuthentication, SessionAuthentication),
		permission_classes=(IsAuthenticated, ))
	def heartbeat(self, request, *args, **kwargs):
		user_dtls_serializer = UserPrimaryDtlsSerializer(instance=self.request.user)
		return Response(user_dtls_serializer.data)

class UserPasswordChangeViewSet(GenericViewSet):
	
	def _validate_password_dtls(self, current_password, new_password, confirmed_new_password):
		if not current_password:
			raise ValidationError("Invalid current password")
		
		if not new_password:
			raise ValidationError("Invalid new password")
			
		if new_password != confirmed_new_password:
			raise ValidationError("New password and its confirmed form are not same")
	
		if new_password == current_password:
			raise ValidationError("Current password and new password are same")
	
	@list_route(methods=["PUT"], permission_classes=(IsAuthenticated, ))
	def changepassword(self, request, *args, **kwargs):
		current_password = request.data.get("current_password", None)
		new_password = request.data.get("new_password", None)
		confirmed_new_password = request.data.get("confirmed_new_password", None)

		self._validate_password_dtls(current_password, new_password, confirmed_new_password)
		
		if not self.request.user.check_password(current_password):
			raise ValidationError("Current password doesn't match with exisiting password")
		
		self.request.user.set_password(new_password)
		self.request.user.save()
		update_session_auth_hash(self.request, self.request.user)
		
		return Response({"status": "success"})


class UserPasswordResetViewSet(GenericViewSet):
	
	@detail_route(methods=["POST"])
	def sendemail(self, request, pk, *args, **kwargs):
		pass

	@detail_route(methods=["POST"])
	def validate_reset_token(self, request, pk, *args, **kwargs):
		pass
	
	@detail_route(methods=["PUT"])
	def resetpassword(self, request, pk, *args, **kwargs):
		pass


class UserTokenViewSet(GenericViewSet, ListModelMixin):
	permission_classes = (IsAuthenticated, )
	queryset = Token.objects.all()
	serializer_class = UserTokenSerializer
	
	def get_queryset(self, *args, **kwargs):
		queryset = super(UserTokenViewSet, self).get_queryset(*args, **kwargs)
		return queryset.filter(user=self.request.user)
