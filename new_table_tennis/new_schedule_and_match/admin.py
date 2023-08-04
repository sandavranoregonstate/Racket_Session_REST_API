from django.contrib import admin

# Register your models here.

from .models import Schedule , TheUser , Location , Drill , Feedback , Match , Result , ScheduleToDrill , MatchToDrill


admin.site.register( TheUser )
admin.site.register( Schedule )

admin.site.register( Location )
admin.site.register( Drill )

admin.site.register( Feedback )
admin.site.register( Match )
admin.site.register( Result )
admin.site.register( ScheduleToDrill )

admin.site.register( MatchToDrill )
