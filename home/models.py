'''Each class in models.py is a table in the database file(db.sqlite.3)
and each variable of the class is a column in the database table.
models.Model adds a column for pk(id) so we need not add it separately.
'''
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#we do not need to add a table for user as it already exists in django

class Subjects(models.Model):
    subjectName = models.CharField(max_length=250) #this is a character field and will store sub name
    subjectLogo = models.FileField() #this is a file fiels which stores an image as sub logo

    '''when a new subject is created by a user, this function will be called which will redirect
    the user to subject details webpage of the subject we just created using its pk'''
    def get_absolute_url(self):
        return reverse('home:subject_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.subjectName #This will show the sub name when we create an object for a subject
                                #in python or Sqlite shell
class FileFolder(models.Model):
    # this column links files to a subject using subject's pk(id)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    folder_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class File(models.Model):
    folder = models.ForeignKey(FileFolder, on_delete=models.CASCADE)#links file to folder
    file = models.FileField()
    description = models.CharField(max_length=5000)
    title = models.CharField(max_length=200)#this is the title given by user to the file
    file_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)#user creating the file
    name = models.CharField(max_length=1000)#this file stores the location of the file
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title

#This table stores discussions
class Discussion(models.Model):
    #column for user which created the discussion
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    #this column links discussion to a subject using subject's pk(id)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    question = models.CharField(max_length=5000)
    anonymous = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    #an optional field to add images to your question
    picture = models.FileField(default='')#optional file-field to add picture

    #when a new discussion is created, return the user to the subject_details page
    def get_absolute_url(self):
        return reverse('home:subject_details', kwargs={'subject_id': self.subject.pk})

    #shows question of the discussion to identify disc. in shell
    def __str__(self):
        return self.title

#table for comments(answers)
class Comments(models.Model):
    #links comments to discussion
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    #links comments to user
    user_comment = models.ForeignKey(User, default=1, on_delete=models.CASCADE)#user creating the comment
    answer = models.CharField(max_length=5000)
    #optional field to add image to comments
    image = models.FileField(default='')#optional file-field to add picture
    anonymous = models.BooleanField(default=False)

    #when a new comment is added, return to subject_details page
    def get_absolute_url(self):
        return reverse('home:subject_details', kwargs={'subject_id': self.discussion.subject.pk})

    #show answer of comments in shell to identify comments
    def __str__(self):
        return self.answer

