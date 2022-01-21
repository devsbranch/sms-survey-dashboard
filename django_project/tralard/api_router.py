from django.conf import settings

from rest_framework.routers import DefaultRouter, SimpleRouter


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    *router.urls,
]

# router.register(
#     "register", 
#     RegisterViewSet, 
#     basename="register"
#     )
# router.register(
#     "login", 
#     LoginViewSet, 
#     basename="login"
#     )


app_name = "tralard"
urlpatterns = router.urls