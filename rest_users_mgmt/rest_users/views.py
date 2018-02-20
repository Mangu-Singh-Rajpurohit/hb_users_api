from django.db import transaction

from rest_framework.decorators import detail_route, list_route
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from rest_users.serializers import UserSignUpSerializer, UserPrimaryDtlsSerializer

# Create your views here.
class UserSignupViewSet(CreateModelMixin, GenericViewSet):
	serializer_class = UserSignUpSerializer

	def create(self, request, *args, **kwargs):
		with transaction.atomic():
			serializer = self.get_serializer_class()(data=request.data)
			serializer.is_valid(raise_exception=True)
			user_instance = serializer.save()
			
			password = request.data["password"]
			user_instance.set_password(password)
			user_instance.save()
			
		# Send email to user's email address asynchronously
			
		user_dtls_serializer = UserPrimaryDtlsSerializer(instance=user_instance)
		return Response(user_dtls_serializer.data, status=HTTP_201_CREATED)

	@list_route(methods=["PUT"])
	def activate(self, request, *args, **kwargs):
		pass


class UserAuthViewSet(GenericViewSet):
	
	@staticmethod
	def login_user(request, *args, **kwargs):
		pass
		
	@list_route(methods=["POST"])
	def session(self, request, *args, **kwargs):
		pass
	
	@list_route(methods=["GET"])
	def token(self, request, *args, **kwargs):
		pass
	
	@list_route(methods=["GET", "POST"])
	def logout(self, request, *args, **kwargs):
		pass


class UserPasswordChangeViewSet(GenericViewSet):
	@detail_route(methods=["PUT"])
	def changepassword(self, request, pk, *args, **kwargs):
		pass


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
