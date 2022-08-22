from .models import Database
from django.forms import ModelForm


class DatabaseForm(ModelForm):
	class Meta:
		model = Database
		fields = '__all__'


class PrimDocForm(ModelForm):
	class Meta:
		model = Database
		fields = ['title', 'database', 'sheet_name', 'skip_row']
