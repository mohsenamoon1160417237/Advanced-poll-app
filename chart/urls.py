from django.urls import path
from . import views



urlpatterns = [

	path('<int:poll_id>/<slug:poll_slug>/' , views.chart , name='chart'),

]