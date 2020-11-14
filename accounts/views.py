from django.shortcuts import render , redirect , get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.views import LoginView
from polls.models import Poll , Choice , UserVotes






class MyLoginView(LoginView):

	template_name = 'registration/login.html'

	def get_context_data(self , **kwargs):

		context = super().get_context_data(**kwargs)
		context.update({

			'section': 'login'
			})

		return context




def user_register(request):

	if request.method == 'POST':

		form = UserRegistrationForm(data=request.POST)

		if form.is_valid():

			cd = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(cd['password2'])

			new_user.save()

			return redirect('home')

	else:

		form = UserRegistrationForm()

	section = 'register'

	return render(request , 'register.html' , {'form':form,
											   'section':section})



@login_required
def home(request):

	user = get_object_or_404(User , username=request.user.username)
	section = 'home'

	polls = Poll.objects.all()

	user_votes = UserVotes.objects.filter(poll__in=polls)

	return render(request , 'home.html' , {'user':user,
										   'section':section,
										   'polls':polls,
										   'user_votes':user_votes})
