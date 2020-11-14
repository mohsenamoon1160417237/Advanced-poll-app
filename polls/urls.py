from django.urls import path
from . import views



urlpatterns = [

	path('choice/<int:choice_id>/<slug:choice_slug>/' , views.choice , name='choice'),
	
	path('poll/<int:poll_id>/<slug:poll_slug>/' , views.poll , name='poll'),
	path('unvote/<int:choice_id>/<slug:choice_slug>/' , views.unvote , name='unvote'),

	path('create_poll/' , views.create_poll , name='create_poll'),


]
