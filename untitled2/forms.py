from django.forms import ModelForm

from PizzaSearch.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'date_comment','pizza', 'user']