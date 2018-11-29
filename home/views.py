'''views.py contains functions/classes(called as functions) which are called when a user
enters a url'''

from .models import Subjects, Discussion, Comments, FileFolder, File
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, SubjectsForm, DiscussionFormIndex, FileForm, CommentsForm, DiscussionFormSub, FoldersForm

FILE_TYPES = ['png', 'jpg', 'jpeg', 'pdf', 'ppt', 'pptx']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

#home page
def index(request):
    #if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    # enter the webpage only if the user is a registered user
    else:
        allSubjects = Subjects.objects.all()
        return render(request, 'home/index.html', {'allSubjects': allSubjects})

#webpage showing discussions in a webpage
def subDetail(request, subject_id):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        #creating variables to store user and subject
        user = request.user
        #using shortcut to raise a 404 error if a subject with pk which doesnot exist in the database is called
        subject = get_object_or_404(Subjects, pk=subject_id)
        #this variable is used by the navigation bar to show list of subjects
        allSubjects = Subjects.objects.all()
        #the dictionary in render function stores all the variables
        return render(request, 'home/subject.html', {'subject': subject, 'user': user, 'allSubjects': allSubjects})

#page showing discussions added by a user
def myDiscussions(request):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        user = request.user
        discussion = Discussion.objects.filter(user=request.user)
        allSubjects = Subjects.objects.all() #this variable is used by the navigation bar to show list of subjects
        return render(request, 'home/myDiscussions.html', {'discussion': discussion, 'user': user, 'allSubjects': allSubjects})

def folders(request, subject_id):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        user = request.user
        subject = get_object_or_404(Subjects, pk=subject_id)
        allSubjects = Subjects.objects.all()
        allFolders = subject.filefolder_set.all()
        return render(request, 'home/folders.html', {'allFolders': allFolders, 'user': user, 'subject': subject, 'allSubjects': allSubjects})

def files(request, folder_id):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        user = request.user
        folder = get_object_or_404(FileFolder, pk=folder_id)
        allSubjects = Subjects.objects.all() #this variable is used by the navigation bar to show list of subjects
        return render(request, 'home/files.html', {'folder': folder, 'user': user, 'allSubjects': allSubjects})

#function to show a webpage showing all the comments of a discussion
def discussion_details(request, discussion_id, subject_id):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        user = request.user
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        subject = get_object_or_404(Subjects, pk=subject_id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        pk = subject_id
        return render(request, 'home/comments.html', {'discussion': discussion, 'subject': subject, 'pk': pk, 'user': user, 'allSubjects': allSubjects})

#create new subjects
def create_subject(request):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        #use SubjectsForm class from forms.py
        form = SubjectsForm(request.POST or None, request.FILES or None)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        '''Only users approved by admin can add subjects, rest will get an error message'''
        if request.user.id is 1:
            if form.is_valid():
                #do not save the form to database now
                subject = form.save(commit=False)
                subject.user = request.user
                subject.subjectLogo = request.FILES['subjectLogo']
                subject.save()#now save the file to database
                #return to homepage
                return render(request, 'home/subject.html', {'allSubjects': allSubjects, 'subject': subject})
            context = {
                "form": form,
                'allSubjects': allSubjects,
            }
            return render(request, 'home/subjects_form.html', context)
        return render(request, 'home/index.html',{'allSubjects': allSubjects, 'error_message': 'You need to be an admin to create subjects. To add this subject, please send an e-mail to srthkdb@iitk.ac.in and your requested subject will be adden soon. '})

#create new subjects
def create_folder(request, subject_id):
    # if user is not a registered user, redirect them to login page
    form = FoldersForm(request.POST or None, request.FILES or None)
    user = request.user
    subject = get_object_or_404(Subjects, pk=subject_id)
    allSubjects = Subjects.objects.all()
    allFolders = subject.filefolder_set.all()
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        '''Only users approved by admin can add subjects, rest will get an error message'''
        if form.is_valid():
            #do not save the form to database now
            folder = form.save(commit=False)
            folder.subject = subject
            folder.folder_user = request.user
            folder.save()#now save the file to database
            #return to homepage
            return render(request, 'home/folders.html', {'allFolders': allFolders, 'user': user, 'subject': subject, 'allSubjects': allSubjects})
        context = {"form": form, 'allSubjects': allSubjects,}
        return render(request, 'home/folders_form.html', context)

#create a discussion from homepage(extra field specifying subject is needed)
def create_discussion_index(request):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        form = DiscussionFormIndex(request.POST or None, request.FILES or None)
        allSubjects = Subjects.objects.all()
        if form.is_valid():
            #do not save to database now
            discussion = form.save(commit=False)
            discussion.user = request.user
            if discussion.picture: #if a picture is uploaded
                file_type = discussion.picture.url.split('.')[-1]#extract it's extension
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:#check for invalid formats
                    context = {
                        'subject': discussion.subject,
                        'form': form,
                        'error_message': 'File format must be .png, .jpg or .jpeg',
                        'allSubjects': allSubjects,
                    }
                    return render(request, 'home/discussion_form.html', context)
            #save to database
            discussion.save()
            return render(request, 'home/subject.html', {'subject': discussion.subject})
        return render(request, 'home/discussion_form.html', {'form': form})

def create_file(request, folder_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        folder = get_object_or_404(FileFolder, pk=folder_id)
        user = request.user
        allSubjects = Subjects.objects.all()  # this variable is used by the navigation bar to show list of subjects
        if form.is_valid():
            file = form.save(commit=False)
            file.folder = folder
            file.file = request.FILES['file']
            file.name = file.file.url
            file_type = file.file.url.split('.')[-1]#extract file format
            file.type = file_type.lower()
            if file.type not in FILE_TYPES:#if invalid format is present
                context = {
                    'folder': folder,
                    'form': form,
                    'error_message': 'File format must be .png, .jpg, .jpeg, .pdf, .txt, .ppt or .pptx',
                    'allSubjects': allSubjects,
                }
                return render(request, 'home/file_form.html', context)

            file.save()
            return render(request, 'home/files.html', {'folder': folder, 'user': user, 'allSubjects': allSubjects})
        context = {
            'folder': folder,
            'form': form,
            'allSubjects': allSubjects,
        }
        return render(request, 'home/file_form.html', context)

#create a discussion from subjects page no need to specify subject.
def create_discussion_sub(request, subject_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        # use DiscussionFormSub class from forms.py
        form = DiscussionFormSub(request.POST or None, request.FILES or None)
        #get subject using its pk so user does not need to fill a form specifying the subject
        subject = get_object_or_404(Subjects, pk=subject_id)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.subject = subject
            discussion.user = request.user
            subject_disucssions = subject.discussion_set.all()
            if discussion.picture:#if a picture is uploaded
                file_type = discussion.picture.url.split('.')[-1]#extract its extension
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:#if file format is not valid
                    context = {
                        'subject': discussion.subject,
                        'form': form,
                        'error_message': 'File format must be .png, .jpg or .jpeg',
                    }
                    return render(request, 'home/discussion_form.html', context)
            discussion.save()
            return render(request, 'home/subject.html', {'subject': subject})
        #compact way to pass dictionary to the render function.
        context = {
            'subject': subject,
            'form': form,
        }
        return render(request, 'home/discussion_form.html', context)

def create_comment(request, subject_id, discussion_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        # use CommentsForm class from forms.py
        form = CommentsForm(request.POST or None, request.FILES or None)
        #import subject and discussion from pk so user does not need to fill separate forms for them
        subject = get_object_or_404(Subjects, pk=subject_id)
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.user_comment = request.user
            if comment.image:#if image is uploaded
                file_type = comment.image.url.split('.')[-1]#extract file format
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:#if invalid format is present
                    context = {
                        'subject': subject,
                        'form': form,
                        'discussion': discussion,
                        'error_message': 'File format must be .png, .jpg or .jpeg',
                        'allSubjects': allSubjects,
                    }
                    return render(request, 'home/comments_form.html', context)
            comment.save()
            return render(request, 'home/comments.html', {'subject': subject, 'discussion':discussion, 'allSubjects':allSubjects})
        context = {
            'subject': subject,
            'discussion': discussion,
            'allSubjects': allSubjects,
            'form': form,
        }
        return render(request, 'home/comments_form.html', context)

#delete a discussion
def delete_discussion(request, subject_id, discussion_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        subject = get_object_or_404(Subjects, pk=subject_id)
        discussion = Discussion.objects.get(pk=discussion_id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        #only user who has created a discussion can delete it.
        if request.user.id is discussion.user.id:
            discussion.delete()
            return render(request, 'home/subject.html', {'subject': subject, 'allSubjects': allSubjects, 'error_message': 'Discussion deleted successfully' })
        return render(request, 'home/subject.html', {'subject': subject, 'allSubjects': allSubjects, 'error_message': "You can only delete discussions you've created"})

def delete_file(request, folder_id, file_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        folder = get_object_or_404(FileFolder, pk=folder_id)
        file = File.objects.get(pk=file_id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        #only user who has created a file can delete it.
        if request.user.id is file.file_user.id:
            file.delete()
            return render(request, 'home/files.html', {'folder': folder, 'allSubjects': allSubjects, 'error_message': 'File deleted successfully' })
        return render(request, 'home/files.html', {'folder': folder, 'allSubjects': allSubjects, 'error_message': "You can only delete files you've uploaded"})

def delete_folder(request, folder_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        folder = get_object_or_404(FileFolder, pk=folder_id)
        subject = Subjects.objects.get(pk=folder.subject.id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        #only user who has created a folder can delete it.
        if request.user.id is folder.folder_user.id:
            folder.delete()
            return render(request, 'home/folders.html', {'subject': subject, 'allSubjects': allSubjects, 'error_message': 'Folder deleted successfully' })
        return render(request, 'home/folders.html', {'subject': subject, 'allSubjects': allSubjects, 'error_message': "You can only delete folders you've uploaded"})

#delete a comment
def delete_comment(request, subject_id, discussion_id, comment_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        subject = get_object_or_404(Subjects, pk=subject_id)
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        comment = Comments.objects.get(pk=comment_id)
        allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
        #only user who has created the comment can delete it
        if request.user.id is comment.user_comment.id:
            comment.delete()
            return render(request, 'home/comments.html', {'discussion': discussion, 'comment': comment, 'subject': subject, 'allSubjects': allSubjects, 'error_message': 'Discussion deleted successfully' })
        return render(request, 'home/comments.html', {'discussion': discussion, 'comment': comment, 'subject': subject, 'allSubjects': allSubjects, 'error_message': "You can only delete comments you've created"})


#register a new user
#this is a class but will be interpreted as a function by django
class UserFormView(View):
    #Credits: code structure for this class is adapted from newboston django video tutorials.
    form_class = UserForm
    template_name = 'home/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            #cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            #add user to the database
            user.save()

            #returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                #django gives admin power to suspend users. This option checks if the user is not suspended.
                if user.is_active:
                    login(request, user)
                    allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
                    return render(request, 'home/index.html', {'allSubjects': allSubjects})
        return render(request, self.template_name, {'form': form})

#in django, request already has the function logout() written, we just have to use it
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'home/login.html', {"form": form})

#logging in a user
def login_user(request):
    #if user is already logged in, return them to homepage
    if request.user.is_authenticated:
        return render(request, 'home/index.html', {'error_message': 'You are already logged in! Click on the Oraculi button on the top left corner of screen'})
    #process form data
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #if user exists
        if user is not None:
            #if user is not suspended
            if user.is_active:
                #login funtion is already in request
                login(request, user)
                allSubjects = Subjects.objects.all()#this variable is used by the navigation bar to show list of subjects
                return render(request, 'home/index.html', {'allSubjects': allSubjects})
            else:
                return render(request, 'home/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'home/login.html', {'error_message': 'Invalid login'})
    return render(request, 'home/login.html')

#post discussion as anonymous
def d_anonymous(request, subject_id):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        subject = get_object_or_404(Subjects, pk=subject_id)
        try:
            selected_discussion = subject.discussion_set.get(pk=request.POST['discussion'])
            #if invalid pk is passed, show error message
        except (KeyError, Discussion.DoesNotExist):
            return render(request, 'home/subject.html', {
                'subject': subject,
                'error_message': "You did not select a valid discussion",
            })
        #if pk is valid, set anonymous to true
        else:
            selected_discussion.anonymous = True #if there are no errors, set anonymous to true
            selected_discussion.save()
            return render(request, 'home/subject.html', {'subject': subject})

#post comments as anonymous
def c_anonymous(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    else:
        try:
            selected_comment = discussion.comments_set.get(pk=request.POST['comment'])
        except (KeyError, Comments.DoesNotExist):
            return render(request, 'home/comments.html', {
                'discussion': discussion,
                'error_message': "You did not select a valid comment",
            })
        else:
            selected_comment.anonymous = True #if there are no errors, set anonymous to true
            selected_comment.save()
            return render(request, 'home/comments.html', {'discussion': discussion})















