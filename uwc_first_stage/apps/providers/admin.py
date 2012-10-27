from django.contrib import admin
from models import Provider


class ProviderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Provider)