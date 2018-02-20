from rest_framework.routers import SimpleRouter

from rest_users.views import UserSignupViewSet, UserAuthViewSet, \
			UserPasswordResetViewSet, UserPasswordChangeViewSet, \
			UserTokenViewSet

user_router = SimpleRouter()
user_router.register("signup", UserSignupViewSet, "signup")
user_router.register("", UserAuthViewSet, "auth")
user_router.register("", UserPasswordChangeViewSet, "password-change")
user_router.register("", UserPasswordResetViewSet, "password-reset")
user_router.register("token", UserTokenViewSet, "user-token")

urlpatterns = user_router.urls