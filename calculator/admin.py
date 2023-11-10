from django.contrib import admin

from calculator.models import Operator


class OperatorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Operator, OperatorAdmin)
