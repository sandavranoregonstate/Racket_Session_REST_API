from django.contrib import admin

# Register your models here.

from .models import Schedule , TheUser , Location , Drill

admin.site.register( TheUser )
admin.site.register( Location )
admin.site.register( Drill )
