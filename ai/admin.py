from django.contrib import admin
from ai import models 

class AIResultAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'result',)
    
admin.site.register(models.AIResult, AIResultAdmin)