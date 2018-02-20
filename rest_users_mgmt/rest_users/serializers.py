from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, ModelSerializer
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class UserSignUpSerializer(ModelSerializer):
	class Meta:
		model = USER_MODEL
		fields = ("username", "email", "password")
		extra_kwargs = {
			"password": {
				"write_only": True
			},
			"email": {
				"required": True
			}
		}


class UserAuthSerializer(Serializer):
	# min-length and max-length must match their corresponding
	# counterparts in User model.
	username = CharField(min_length=1, max_length=30)
	password = CharField(min_length=1, max_length=30)
	
	class Meta:
		fields = ("username", "password")
		extra_kwargs = {
			"password": {
				"write_only": True
			}
		}


class UserPrimaryDtlsSerializer(ModelSerializer):
	class Meta:
		model = USER_MODEL
		fields = ("id", "username", "email")
		read_only_fields = ("id", )
