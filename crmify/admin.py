from django.contrib import admin
from crmify import models


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'external_id', 'external_status', 'anchor', 'last_synced',)
    readonly_fields = ('external_id', 'last_synced',)


admin.site.register(models.Lead, LeadAdmin)