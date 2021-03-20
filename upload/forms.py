from django import forms 
from .models import *
class DocumentForm(forms.ModelForm):
    image_path = forms.ImageField(label='',
                    widget=forms.ClearableFileInput(
                        attrs={
                            "class" : "form-control",
                            "id" : "img",
                            "onchange" : "validateImage('img')",
                            
                        }
                    )
                )
    message = forms.CharField(label='',
                widget=forms.Textarea(
                        attrs={
                            "class" : "form-control",
                            "placeholder" : "Enter your message here",
                            "cols" : "1",
                            "rows" : "2"
                        }
                )
            )
    class Meta:
        model=Document
        fields={'message','image_path',}   


class forms_imgenc(forms.ModelForm):
    main_img = forms.CharField(label='Hide Image',
                widget=forms.ClearableFileInput(
                        attrs={
                            "class" : "form-control",
                            "id" : "image1",
                            "onchange" : "validateImage('image1')"
                        }
                    )   
                )
    cover_img = forms.CharField(label='Cover Image',
                widget=forms.ClearableFileInput(
                        attrs={
                            "class" : "form-control",
                            "id" : "image2",
                            "onchange" : "validateImage('image2')"
                        }
                    )
                )
    class Meta:
        model = img_steg_enc
        fields = ('main_img','cover_img',)

