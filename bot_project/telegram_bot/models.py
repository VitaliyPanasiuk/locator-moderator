from django.db import models


class Chats(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, verbose_name="ID чата Telegram")
    chat_name = models.CharField(max_length=255, verbose_name="Название чата")
    stop_word_file = models.FileField(
        upload_to='stop_words/',
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Файл со стоп-словами"
    )

    class Meta:
        managed = False
        db_table = 'chats'
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"



class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True, verbose_name="ID пользователя Telegram")
    user_name = models.TextField(blank=True, null=True, verbose_name="Имя пользователя")
    can_forward = models.BooleanField(default=False, verbose_name="Разрешить пересылку")
    can_send_links = models.BooleanField(default=False, verbose_name="Разрешить ссылки")
    can_send_photos = models.BooleanField(default=False, verbose_name="Разрешить фото")
    can_send_videos = models.BooleanField(default=False, verbose_name="Разрешить видео")
    can_send_files = models.BooleanField(default=False, verbose_name="Разрешить файлы")
    can_send_gifs_stickers = models.BooleanField(default=False, verbose_name="Разрешить GIF и стикеры")
    can_send_voice = models.BooleanField(default=False, verbose_name="Разрешить голосовые/кружки")

    class Meta:
        managed = False
        db_table = 'users' 
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
