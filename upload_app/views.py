from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Database
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
from .forms import DatabaseForm, PrimDocForm
import pandas as pd
import json

# Create your views here.


# class DatabaseCreate(CreateView):
#     # Модель куда выполняется сохранение
#     model = Database
#     # Класс на основе которого будет валидация полей
#     form_class = DatabaseForm
#     # Выведем все существующие записи на странице
#     extra_context = {'databases': Database.objects.all()}
#     # Шаблон с помощью которого
#     # будут выводиться данные
#     template_name = 'database.html'
#     # На какую страницу будет перенаправление
#     # в случае успешного сохранения формы
#     success_url = '/database/'


def database(request):
    status_info = {
        'warning': {'type': 'warning', 'class': "alert alert-danger", 'message': "Sorry, it's not Excel file:"},
        'info': {'type': 'info', 'class': "alert alert-info", 'message': "It's OK. File upload: "},
        'error': {'type': 'error', 'class': "alert alert-danger", 'message': "It's NOT OK. File isn't upload."},
    }
    data = Database.objects.filter(user=request.user.id).order_by('-published')
    is_excel = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    if request.method == 'POST':
        form = PrimDocForm(request.POST, request.FILES)
        if form.is_valid():
            name_file = str(request.FILES['database'].name)
            if request.FILES['database'].content_type != is_excel:
                return render(request, 'database.html',
                              {'form': form,
                               'status_info': status_info['warning'],
                               'name_file': name_file,
                               'data': data
                               })
            else:
                file_in = request.FILES['database'].file
                sheet_name = request.POST['sheet_name']
                skip_row = request.POST['skip_row']
                # import pdb; pdb.set_trace()
                status_df, df_table, df = df_return(file_in, sheet_name, skip_row)

                if status_df == 'ok':
                    fields = form.save(commit=False)
                    try:
                        fields.user = request.user
                        fields.save()
                        return render(request, 'database.html',
                                      {'table': df,
                                       'status_info': status_info['info'],
                                       'name_file': name_file,
                                       'data': data,
                                       'form': form,
                                       })
                    except ValueError:
                        return render(request, 'database.html',
                                      {'table': df,
                                       'status_info': status_info['info'],
                                       'name_file': name_file,
                                       'data': data,
                                       'form': form,
                                       })
                elif status_df == 'error':
                    return render(request, 'database.html',
                                  {'form': form,
                                   'status_info': status_info['error'],
                                   'name_file': name_file,
                                   'data': data,
                                   })
    else:
        form = PrimDocForm()
        return render(request, 'database.html', {'data': data, 'form': form})


def database_in(request, database_id):
    data = Database.objects.filter(id=database_id)
    status_df, df_table, df = df_return(data[0].database, data[0].sheet_name, data[0].skip_row)
    json_records = df_table.reset_index().to_json(orient='records')
    df_table_json = json.loads(json_records)
    # import pdb; pdb.set_trace()
    return render(request, 'database_in.html', {'data': data, 'table': df, 'df_table_column': df_table_json[0]})


def upload(request):
    status_info = {
        'warning': {'type': 'warning', 'class': "alert alert-danger", 'message': "Sorry, it's not Excel file:"},
        'info': {'type': 'info', 'class': "alert alert-info", 'message': "It's OK. File upload: "},
        'error': {'type': 'error', 'class': "alert alert-danger", 'message': "It's NOT OK. File isn't upload."},
    }
    is_excel = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    if request.method == 'POST':
        form = PrimDocForm(request.POST, request.FILES)
        if form.is_valid():
            name_file = str(request.FILES['database'].name)
            if request.FILES['database'].content_type != is_excel:

                return render(request, 'upload.html',
                              {'form': form,
                               'status_info': status_info['warning'],
                               'name_file': name_file,
                               })
            else:
                file_in = request.FILES['database'].file
                sheet_name = request.POST['sheet_name']
                skip_row = request.POST['skip_row']
                status_df, df_table, df = df_return(file_in, sheet_name, skip_row)
                if status_df == 'ok':
                    # status_key = status_info[status_dict['status']]
                    # message = status_dict['message']
                    # status = f'<div class = "{status_key}" role="alert">{message}</div>'
                    fields = form.save(commit=False)
                    # import pdb; pdb.set_trace()
                    try:
                        fields.user = request.user
                        fields.save()
                        return render(request, 'upload.html',
                                      {'table': df,
                                       'status_info': status_info['info'],
                                       'name_file': name_file,
                                       })
                    except ValueError:
                        return render(request, 'upload.html',
                                      {'table': df,
                                       'status_info': status_info['info'],
                                       'name_file': name_file,
                                       })
                elif status_df == 'error':
                    return render(request, 'upload.html', {'form': form,
                                                           'status_info': status_info['error'],
                                                           'name_file': name_file,
                                                           })
    else:
        form = PrimDocForm()
    # import pdb;	pdb.set_trace()
    return render(request, 'upload.html', {'form': form, 'status': 'First'})


def df_return(file, sheet_name, skip_row):
    try:
        df = pd.read_excel(io=file, sheet_name=int(sheet_name), skiprows=int(skip_row))
        status = 'ok'
        return status, df, df.to_html(border=0,
                                  justify='center',
                                  classes=['table', 'align-middle', 'caption-top',
                                           'table-striped', 'table-bordered', 'table-responsive-sm'],
                                  index=False).replace('<tbody>', '<tbody style="text-align: center">')
    except:
        status = 'error'
        return status, ''


def home_page(request):
    # POST - обязательный метод
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(filename)
        return render(request, 'home_page.html', {
            'file_url': file_url
        })
    return render(request, 'home_page.html')
