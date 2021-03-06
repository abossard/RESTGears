from django.contrib import admin
#from django.contrib.auth.models import User
from permission_backend_nonrel.admin import NonrelPermissionCustomUserAdmin

from account.models import DeviceAuthToken, UserProfile, User
from django.contrib.auth.models import Group, User as BaseUser

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class DeviceAuthTokenInline(admin.TabularInline):
    model = DeviceAuthToken
    fields = ('unique_id', 'ip_address','user_agent', 'authenticated_on', 'banned',)
    readonly_fields = ('unique_id', 'ip_address','user_agent', 'authenticated_on', )
    extra = 0

class CustomUserAdmin(NonrelPermissionCustomUserAdmin):
    inlines = [UserProfileInline,DeviceAuthTokenInline,]
    
admin.site.unregister(BaseUser)
admin.site.register(BaseUser, CustomUserAdmin)

class DeviceAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('unique_id','user','ip_address','authenticated_on', 'banned',)
    list_editable = ('banned',)
    fields = ('unique_id', 'ip_address','user_agent', 'authenticated_on', 'banned',)
    readonly_fields = ('unique_id', 'ip_address','user_agent', 'authenticated_on', )
    list_filter = ('banned',)

admin.site.register(DeviceAuthToken, DeviceAuthTokenAdmin)

