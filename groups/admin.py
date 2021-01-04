from django.contrib import admin
from .models import VisitorGroup, Visitor, IntervallDate, ChurchDayVisitorGroup

admin.site.register(VisitorGroup)
admin.site.register(Visitor)
admin.site.register(IntervallDate)
admin.site.register(ChurchDayVisitorGroup)

