from .views import BookViewSet,HomeView,RegisterUser,Login,UserDetail
from django.urls import path,include

app_name='api'
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
router=DefaultRouter()

router.register(r'epicbooks', BookViewSet,basename='Books')

urlpatterns = [
    path('',include(router.urls)),
    path('home/',HomeView.as_view(),name='home'),
    path('register/',RegisterUser.as_view(),name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('profile/',UserDetail.as_view(),name='detail'),
    path('gettoken/',TokenObtainPairView.as_view(),name='token_obtain_view'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='token_refresh'),
    path('verifytoken/',TokenVerifyView.as_view(),name='token_verify'),
]

