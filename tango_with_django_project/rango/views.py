from django.shortcuts import render
from django.http import HttpResponse

def index(request):
# sending the bold message to the server:
	context = {'boldmessage' : "I am shahjahan, from context"}
	return render(request,'rango/index.html',context)

def about(request):
	return HttpResponse("Rango says here is the about page. Click <a href='../'> here</a>")
 