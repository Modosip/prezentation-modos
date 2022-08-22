from django.shortcuts import render, redirect


def dbtemplates(request):
	return render(request, 'templates.html')
