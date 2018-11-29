#this files tells which function/class to call form views.py when the user enters one of the following specified urls
from django.conf.urls import url
from . import views

app_name = 'home' #this app name helps to distinguish eg index.html files of different apps while referencing utls

urlpatterns = [
    #/home/
    url(r'^$', views.index, name='index'),
    #/home/my_discussions
    url(r'^my_discussions/$', views.myDiscussions, name='my_discussions'),
    #/home/login_user
    url(r'^login_user/$', views.login_user, name='login_user'),
    #/home/logout_user
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    #/home/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),#using .as_view() so django interprets class as a function
    #/home/<subject_id>
    url(r'^(?P<subject_id>[0-9]+)/$', views.subDetail, name="subject_details"),
    # /home/<subject_id>/folders
    url(r'^(?P<subject_id>[0-9]+)/folders/$', views.folders, name="folders"),
    # /home/<folder_id>/files
    url(r'^(?P<folder_id>[0-9]+)/files/$', views.files, name="files"),
    # /home/<folder_id>/folder/delete_folder/
    url(r'^(?P<folder_id>[0-9]+)/folder/delete_folder/$', views.delete_folder, name="delete_folder"),
    # /home/<folder_id>/<file_id>/file/delete_file/
    url(r'^(?P<folder_id>[0-9]+)/(?P<file_id>[0-9]+)/file/delete_file/$', views.delete_file, name="delete_file"),
    # /home/<folder_id>/files/create/
    url(r'^(?P<folder_id>[0-9]+)/files/create/$', views.create_file, name="create_file"),
    # /home/<subject_id>/create_folders/
    url(r'^(?P<subject_id>[0-9]+)/create_folders/$', views.create_folder, name="create_folder"),
    #/home/<discussion_id>/<subject_id>/
    url(r'^(?P<discussion_id>[0-9]+)/(?P<subject_id>[0-9]+)/$', views.discussion_details, name="discussion_details"),
    #/home/subjects/add/
    url(r'^subjects/add/$', views.create_subject, name="subject-add"),
    #/home/<subject_id>/create_discussion/  (checks subject_id)
    url(r'^(?P<subject_id>[0-9]+)/create_discussion/$', views.create_discussion_sub, name="discussion-add"),
    #/home/create_discussion/
    url(r'^create_discussion/$', views.create_discussion_index, name="discussion-add-index"),
    #/home/subjects/<subject_id>/<discussion_id/delete_discussion
    url(r'^discussion/(?P<subject_id>[0-9]+)/(?P<discussion_id>[0-9]+)/delete_discussion/$', views.delete_discussion, name="discussion-delete"),
    #/home/<subject_id>/<discussion_id>/create_comment/
    url(r'^(?P<subject_id>[0-9]+)/(?P<discussion_id>[0-9]+)/create_comment/$', views.create_comment, name="comments-add"),
    # /home/<subject_id>/<discussion_id>/<comment_id>/delete_comment/
    url(r'^discussion/(?P<subject_id>[0-9]+)/(?P<discussion_id>[0-9]+)/(?P<comment_id>[0-9]+)/delete_comment/$', views.delete_comment, name="comment-delete"),
]

