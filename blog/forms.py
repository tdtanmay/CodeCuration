from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'richtexteditor'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30,
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "First Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "First Name"}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Your name:"
        self.fields['email'].label = "Your email:"
        self.fields['message'].label = "What do you want to say?"




# class ContactForm(forms.Form):
#     contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
#     contact_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
#     content = forms.CharField(
#         required=True,
#         widget=forms.Textarea(attrs={'placeholder': 'Message'}))
#
#     # the new bit we're adding
#     def __init__(self, *args, **kwargs):
#         super(ContactForm, self).__init__(*args, **kwargs)
#         self.fields['contact_name'].label = "Your name:"
#         self.fields['contact_email'].label = "Your email:"
#         self.fields['content'].label = "What do you want to say?"