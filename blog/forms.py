from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề...'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }