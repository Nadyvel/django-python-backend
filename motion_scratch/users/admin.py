from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from posts.models import Post
from users.models import User, FriendRequest


class PostInline(admin.TabularInline):
    model = Post


class FriendRequestReceiverInline(admin.TabularInline):
    model = FriendRequest
    fk_name = 'receiver'


class FriendRequestRequesterInline(admin.TabularInline):
    model = FriendRequest
    fk_name = 'requester'


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ('date_joined',)
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty',),
            'fields': ('email', 'username', 'password1', 'password2',)}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups', {'fields': ('groups',)}),
        ('Social', {'fields': ('followed_by', 'i_follow')}),

    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)

    inlines = [
        PostInline,
        FriendRequestReceiverInline,
        FriendRequestRequesterInline
    ]


admin.site.register(FriendRequest)