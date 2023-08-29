from django.contrib import admin

from docsearch import models

admin.site.site_header = 'Forest Preserve of Cook County Document Search Admin'
admin.site.site_title = 'Document Search'

class NotificationSubscriptionAdmin(admin.ModelAdmin):
  list_display = ["user"]
admin.site.register(models.NotificationSubscription, NotificationSubscriptionAdmin)
