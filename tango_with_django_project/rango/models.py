from __future__ import unicode_literals
from django.template.defaultfilters import slugify

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# the category models

class Category(models.Model):
	"""here goes category model"""

	name = models.CharField(max_length=128,unique = True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		
		# Uncomment if you don't want the slug to change every time the name changes
		#if self.id is None:
		#self.slug = slugify(self.name)
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def	__unicode__(self):
		return self.name
# the page model

class Page(models.Model):
		category = models.ForeignKey(Category)
		title = models.CharField(max_length=128)
		url = models.URLField()
		views = models.IntegerField(default=0)

		def __unicode__(self):
			return self.title

class UserProfile(models.Model):

    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(blank=True)

    def __unicode__(self):
    	return self.user.username
    	
    