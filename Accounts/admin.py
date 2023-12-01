from django.contrib import admin
from django.contrib.auth import get_user_model
UserModel = get_user_model()

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    model = UserModel
    list_display = "email", "first_name", "last_name", "country", "phone_number"
    list_display_links = "email", "first_name"