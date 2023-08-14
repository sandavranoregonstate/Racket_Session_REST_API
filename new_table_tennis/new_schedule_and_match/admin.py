from django.contrib import admin

# Register your models here.

from .models import Schedule , TheUser , Location , Feedback , Match


admin.site.register( TheUser )
admin.site.register( Schedule )

admin.site.register( Location )

admin.site.register( Feedback )
admin.site.register( Match )
