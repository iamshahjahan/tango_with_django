from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page, UserProfile
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User


def index(request):
# sending the data from category model to the server:

    context_catogaries = Category.objects.order_by('-likes')[:18]
    context_pages = Page.objects.order_by('-views')[:18]

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

# defining form data
def add_category(request):
    # check for post method

    if request.method == 'POST':
        # means you submitted the form.
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request,'rango/add_category.html',{'form' : form})

# adding page here
def add_page(request,category_name_slug=None):
    # check for post method
    print category_name_slug
    try:
        cat = Category.objects.get(slug = category_name_slug)
    except Exception, e:
        cat = None


    if request.method == 'POST':
        print "sjhdfkjsdhkfhjs"
        # means you submitted the form.
        form = PageForm(request.POST)
        a = form.is_valid()
        if a:
            if cat:
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.save()
                print "sdjhfjshk"
                return HttpResponseRedirect('rango/category/' + category_name_slug + '/')
        else:
            print form.errors

    else:
        form = PageForm()

    context_dict = {'form' : form,'category' : cat, 'slug': category_name_slug}

    return render(request,'rango/add_page.html', context_dict)


def register(request):
	print "hello from request"

	registered = False

	if request.method == 'POST':

		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:
			print user_form.errors , profile_form.errors
	else:
		print " I am in else"
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,'rango/register.html',{'user_form' : user_form,'profile_form' : profile_form,'registered':registered})
