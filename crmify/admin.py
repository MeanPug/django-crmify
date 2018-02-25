from django.contrib import admin
from crmify import models


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'external_id',)
    readonly_fields = ('external_id',)


admin.site.register(models.Lead, LeadAdmin)