from django.contrib import admin
from .models import Users, Chats

@admin.register(Users)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'user_name',  'can_forward', 'can_send_links',
        'can_send_photos', 'can_send_videos', 'can_send_files', 'can_send_gifs_stickers', 'can_send_voice'
    )
    search_fields = ('user_name', 'user_id')
    list_filter = (
        'can_forward', 'can_send_links', 'can_send_photos',
        'can_send_files', 'can_send_gifs_stickers', 'can_send_voice'
    )

@admin.register(Chats)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'chat_name', 'stop_word_file')
    search_fields = ('chat_name', 'chat_id')