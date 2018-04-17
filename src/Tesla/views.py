from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


def home_page(request):
	context = {
		"content": "Welcome to the home page"
	}
	if request.user.is_authenticated:
	 context["premium_content"] = "Yeahhhhhhh"
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
		"title": "About Page",
		"content": "Welcome to the about page"
	}
	return render(request, "about_page.html", context)

def help_page(request):
	context = {
		"title": "Help Page",
		"content": "Welcome to the help page"
	}
	return render(request, "help_page.html", context)