
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('verify-otp',views.verify_otp,name="verify_otp"),
    
]

