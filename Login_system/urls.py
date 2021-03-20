from django.contrib import admin
from django.urls import path
from Login_system import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path("Upload_imgdec/",views.unmerge,name="img_dec"),
    path("Login",views.login,name="login"),
    path("Register",views.signup,name="signin"),
    path("Logout",views.logout,name="logout"),
    path("Forgot_password",views.forgot_pass,name="password"),
    path("Check_otp",views.check_user_otp,name="password"),
    path("change_password",views.change_password,name="password"),

    
    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

