from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Addr)
admin.site.register(Cat)
admin.site.register(CatRel)
admin.site.register(Checkcat)
admin.site.register(Feed)
admin.site.register(Food)
admin.site.register(Sterilize)
admin.site.register(Userinfo)
