from django import forms
from .models import Poll , Choice
from django.forms import formset_factory


class PollCreateForm(forms.ModelForm):

	class Meta:

		model = Poll
		fields = ['name' , 'question' , 'image' , 'vote_limit']

		labels = {

			'name': "Name",
			'question': "Enter your poll's main question",
			'image': "you can upload an image for your poll" ,
			'vote_limit': "How many votes the the voters can take place in your poll?"
		}


	def __init__(self , *args , **kwargs):

		super(PollCreateForm,self).__init__(*args , **kwargs)

		name = self.fields['name']
		question = self.fields['question']
		image = self.fields['image']
		vote_limit = self.fields['vote_limit']

		name.widget.attrs.update({'class':'name-field'})
		question.widget.attrs.update({'class':'question-field'})
		image.widget.attrs.update({'class':'image-field'})
		vote_limit.widget.attrs.update({'class':'vote-field'})



class ChoiceForm(forms.ModelForm):


	class Meta:

		model = Choice
		fields = ['field']

		labels = {

			'field':'Enter your choice'
		}

	def __init__(self , *args , **kwargs):

		super(ChoiceForm,self).__init__(*args , **kwargs)

		field = self.fields['field']

		field.widget.attrs.update({'class' : 'field'})


ChoiceFormset = formset_factory(ChoiceForm , extra=5)