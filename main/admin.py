from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Price)
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Complaints)
admin.site.register(Voilation)





class AddContactsInLineAdmin(admin.TabularInline):
    model = AdditionalContact


class ComplaintsInLineAdmin(admin.TabularInline):
    model = Complaints


class VoilationsInLineAdmin(admin.TabularInline):
    model = Voilation


class PropertyInLineAdmin(admin.TabularInline):
    model = Property


class PropertyAdmin(admin.ModelAdmin):

    inlines = [ComplaintsInLineAdmin,
               VoilationsInLineAdmin, AddContactsInLineAdmin]


# admin.site.register(Membership)
# admin.site.register(UserMembership)
# admin.site.register(Subscription)
admin.site.register(Property, PropertyAdmin)


class UserAdmin(admin.ModelAdmin):

    inlines = [PropertyInLineAdmin]


# admin.site.register(Membership)
# admin.site.register(UserMembership)
# admin.site.register(Subscription)
admin.site.register(User, UserAdmin)
