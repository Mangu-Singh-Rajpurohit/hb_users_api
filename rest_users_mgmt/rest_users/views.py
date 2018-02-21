import logging

from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from rest_users.serializers import UserSignUpSerializer, UserPrimaryDtlsSerializer, \
				UserAuthSerializer, UserTokenSerializer

LOGGER = logging.getLogger("root")


class UserSignupViewSet(CreateModelMixin, GenericViewSet):
	serializer_class = UserSignUpSerializer
	authentication_classes = ()

	def create(self, request, *args, **kwargs):
		LOGGER.debug("Received request for creating user")
		with transaction.atomic():
			serializer = self.get_serializer_class()(data=request.data)
			serializer.is_valid(raise_exception=True)
			user_instance = serializer.save()
			
			password = request.data["password"]
			user_instance.set_password(password)
			user_instance.save()
		
			#create token for newly created user
			LOGGER.debug("creating token for user")
			
			user_token = Token(user=user_instance)
			user_token.save()
			
			LOGGER.debug("Created token for user")
		
		# Send email to user's email address asynchronously
		
		user_dtls_serializer = UserPrimaryDtlsSerializer(instance=user_instance)
		LOGGER.info("User: %s created successfully", user_instance.username)
		
		return Response(user_dtls_serializer.data, status=HTTP_201_CREATED)

	@list_route(methods=["PUT"])
	def activate(self, request, *args, **kwargs):
		pass

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
	
	def _validate_password_dtls(current_password, new_password, confirmed_new_password):
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
		
		self.user.set_password(new_password)
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
