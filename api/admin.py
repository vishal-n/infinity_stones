from django.contrib import admin
from .models import User, Stone, Activation

# Register your models here.
admin.site.register(User)
admin.site.register(Stone)
admin.site.register(Activation)
