from django.contrib import admin

# Register your models here.
from .models import Datasave
from .models import Blogpost
admin.site.register(Datasave)
admin.site.register(Blogpost)