from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class UserSignUpSerializer(ModelSerializer):
	class Meta:
		model = USER_MODEL
		fields = ("username", "email", "password")
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
