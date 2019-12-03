from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Note)
admin.site.register(User_Note)
admin.site.register(Follower)
admin.site.register(Subject)
admin.site.register(Star)
admin.site.register(Collection)
admin.site.register(Recommend)

