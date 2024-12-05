from django.contrib import admin


from django.contrib import admin
from .models import*

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(shortQuestion)
admin.site.register(Chapter)
admin.site.register(MCQ)
admin.site.register(LongQuestion)
