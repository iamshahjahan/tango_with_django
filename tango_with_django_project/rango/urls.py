from django.conf.urls import patterns,url
from rango import views
from django.conf import settings

urlpatterns = patterns('',url(r'^$',views.index,name='index')
						 ,url(r'^about/$',views.about,name='about')
						 ,url(r'^add_category/$',views.add_category,name='add_category')
						 ,url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.category, name ='category')
						 ,url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page, name ='add_page')

						 )
# urlpatterns = patterns('',)
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )