from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category,Page

def index(request):
# sending the data from category model to the server:

	context_catogaries = Category.objects.order_by('-likes')[:5]
	context_pages = Page.objects.order_by('-views')[:5]

	context_dict = {'categories' : context_catogaries , 'pages' : context_pages}

	return render(request,'rango/index.html',context_dict)

def about(request):
	return HttpResponse("Rango says here is the about page. Click <a href='../'> here</a>")
 # working here for the category page

def category(request,category_name_slug):
 	context_dict = []

 	try:
 		c = Category.objects.get(slug = category_name_slug)


		# context_dict['category_name'] = c.name

		pages = Page.objects.filter(category = c)

		for page in pages:
			print page.title

		# context_dict['pages'] = pages
		# context_dict['category'] = c
		context_dict = {'category_name' : c.name,'pages':pages,'category':c} 

	except Exception, e:
		print e
		pass

	return render(request,'rango/category.html',context_dict)