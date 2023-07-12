from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [ 'title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('title')
        description = cleaned_data.get('text')

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
