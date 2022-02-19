from django.forms import ModelForm

from .models import Post
from .models import Profile

from django import forms

class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
        labels = {
         'title': '',
         'content' : ''
                }
        widgets = {

                'title' :forms.TextInput(attrs={'style': 'width:50rem','class' :'form-control', 'placeholder' :'Title' }),
                'content':forms.Textarea(attrs={'style': 'width:50rem; height:10rem', 'class' :'form-control', 'placeholder' :'Content'})

            }


            
class ToFollow(ModelForm):
    class Meta:
        model = Profile
        fields = []