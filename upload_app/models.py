import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
	return 'user_{0}/image/{1}'.format(instance.user.id, filename)


def user_directory_path_db(instance, filename):
	return 'user_{0}/db/{1}'.format(instance.user.id, filename)


class Database(models.Model):
	user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
	title = models.CharField(max_length=150, verbose_name='Название')
	# cover = models.ImageField(upload_to=user_directory_path, verbose_name='Рисунок')
	database = models.FileField(upload_to=user_directory_path_db, verbose_name='База данных')
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата')
	sheet_name = models.IntegerField(verbose_name='Имя листа', default=0)
	skip_row = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Базы данных'
		verbose_name = 'База данных'
		ordering = ['published']

	def __str__(self):
		return self.title

	def filename(self):
		return os.path.basename(self.database.name)


class SliceBase(models.Model):
	db_parent = models.ForeignKey(to=Database, null=False, on_delete=models.PROTECT,
	                              verbose_name='База выбранных данных')
	title = models.CharField(max_length=150, verbose_name='Название базы данных')
	json_db = models.JSONField(verbose_name='Данные JSON')
	filter = models.JSONField(default=dict, verbose_name='Фильтр(поле-значение)')
	sorting = models.JSONField(default=dict, verbose_name='Последовательность сортировки')
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата')

	class Meta:
		verbose_name_plural = 'Slice'
		verbose_name = 'Slices'
		ordering = ['published']

	def __str__(self):
		return self.title
