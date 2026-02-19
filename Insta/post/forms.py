from django import forms
from post.models import post_save, Post, Comment

class NewPostform(forms.ModelForm):
    
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    #tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption']
        
class NewCommentForm(forms.ModelForm):
     body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Drop a comment!'}), required=True)

     class Meta:
        model = Comment
        fields = ['body']

