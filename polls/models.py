from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse



class Poll(models.Model):

	name = models.CharField(max_length=255 , unique=True)
	owner = models.ForeignKey(User , on_delete=models.DO_NOTHING , related_name='polls' , null=True)
	question = models.CharField(max_length=75)
	created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(blank=True , unique=True)
	users = models.ManyToManyField(User, blank=True)
	total = models.IntegerField(default=0)
	image = models.ImageField(upload_to='choices' , blank=True , null=True)
	vote_limit = models.PositiveIntegerField(default=1)


	def __str__(self):

		return self.name

	class Meta:

		ordering = ['-created']

	def save(self , *args , **kwargs):

		self.slug = slugify(self.name)
		return super(Poll,self).save()

	def get_absolute_url(self):

		return reverse('poll' , args=[self.id , self.slug])

	def get_total_votes(self):

		return [sum(i) for i.total in self.choices]
		


class Choice(models.Model):

	poll = models.ForeignKey(Poll , related_name='choices' , on_delete=models.CASCADE , null=True)
	field = models.CharField(max_length=100)
	total = models.IntegerField(default=0)
	users = models.ManyToManyField(User, blank=True)
	slug = models.SlugField(blank=True)



	def __str__(self):

		return '{} : {}'.format(self.poll , self.field)

	class Meta:

		ordering = ['field']

	def save(self , *args , **kwargs):

		self.slug = slugify(self.field)
		return super(Choice,self).save()



class UserVotes(models.Model):

	user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='polls_voted' , null=True)
	user_ip = models.CharField(max_length=100 , null=True)
	poll = models.ForeignKey(Poll , on_delete=models.CASCADE , related_name='polls_voted')
	total = models.PositiveIntegerField(default=0)

	def __str__(self):

		return '{} : {}'.format(self.user , self.poll)

	class Meta:

		verbose_name_plural = 'User votes'

