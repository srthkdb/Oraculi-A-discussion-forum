from django.contrib import admin
from .models import Subjects, Discussion, Comments, FileFolder, File

#these are the classes(tables of database) which can be viewed from django admin panel
admin.site.register(Subjects)
admin.site.register(Discussion)
admin.site.register(Comments)
admin.site.register(FileFolder)
admin.site.register(File)
