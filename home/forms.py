from django import forms
from django.contrib.auth.models import User
from .models import Subjects, Discussion, Comments, FileFolder, File

#this file is for tweaking the default UserForm to remove useless fiels and add new forms.

class UserForm(forms.ModelForm):
    #this tells django is password is a password field
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        #user model already exists in django
        model = User
        #use only given fields and omit useless fields like DOB, first name etc.
        fields = ['username', 'email', 'password']

class SubjectsForm(forms.ModelForm):

    class Meta:
        model = Subjects
        fields = ['subjectName', 'subjectLogo']


class DiscussionFormIndex(forms.ModelForm):
    #this class has a field for subject as subject.id cannot be imported.
    class Meta:
        model = Discussion
        fields = ['subject', 'question', 'title', 'picture', 'anonymous']

    #this function makes adding picture optional
    def __init__(self, *args, **kwargs):
        # credits: function used from stackoverflow
        super(DiscussionFormIndex, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

class DiscussionFormSub(forms.ModelForm):
    #this class has no field for subject as subject.id can be requested from the subject's webpage.
    class Meta:
        model = Discussion
        fields = ['question', 'title', 'picture', 'anonymous']

    # this function makes adding picture optional
    def __init__(self, *args, **kwargs):
        # credits: function used from stackoverflow
        super(DiscussionFormSub, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['answer', 'image', 'anonymous']

    # this function makes adding picture optional
    def __init__(self, *args, **kwargs):
        # credits: function used from stackoverflow
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class FoldersForm(forms.ModelForm):

    class Meta:
        model = FileFolder
        fields = ['name']

class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file', 'description', 'title']