
from django.urls import path
from upload import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #path("test",views.test),
    path("main",views.encode_msg,name="encode"),
    path("decode",views.decode,name="decode"),
    path("Upload_imgenc/",views.merge,name="img_enc"),
    path("check_security",views.check_pin,name="checkpin"),
    path("decode_img",views.decode_img),
    path("dec",views.dec),
    path("encoded_data",views.encoded_data,name="encode")


    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


