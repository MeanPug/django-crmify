from django.contrib import admin
from sales import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['auth', 'address', 'city', 'state']
    fields = ['auth', 'address', 'city', 'state']


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    fields = ['user', 'type']


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)