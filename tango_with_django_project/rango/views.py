from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page, UserProfile
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib


def index(request):

	# check whether cookie exits
	visits = (int(request.COOKIES.get('visits',1)))
	#Create a CookieJar object to hold the cookies
	cj = cookielib.CookieJar()
	#Create an opener to open pages using the http protocol and to process cookies.
	opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

	#create a request object to be used to get the page.
	req = Request("http://www.twitter.com")
	f = opener.open(req)

	#see the first few lines of the page
	html = f.read()
	print html[:50]

	#Check out the cookies
	print "the cookies are: "
	for cookie in cj:
		print cookie


	context_catogaries = Category.objects.order_by('-likes')[:18]
	context_pages = Page.objects.order_by('-views')[:18]
	context_dict = {'categories':context_catogaries,'pages':context_pages}
	response = render(request,'rango/index.html',context_dict)

	visits+=1

	response.set_cookie('visits',visits)

	print "visit is " + str(visits)

	return response
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
@login_required
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
@login_required
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
                return HttpResponseRedirect('/rango/category/' + category_name_slug + '/')
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

def user_login(request):
	if request.method == "POST":
# get username and password
		username = request.POST.get('username')
		password = request.POST.get('password')

 		user = authenticate(username = username,password = password)

 		if user:

 			# check whether user is active or not

 			if user.is_active:
 				login(request,user)

 				return HttpResponseRedirect("/rango/")
 			else:
 				return HttpResponse("Your account has been disabled.")

 		else:
 			print "invalid login details: %s %s" % (username,password)
           	return HttpResponse("Invalid login details supplied.")
 	else:
 		return render(request,'rango/login.html',{})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')