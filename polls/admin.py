from django.contrib import admin
from .models import Poll , Choice , UserVotes



class ChoiceTabular(admin.TabularInline):

	model = Choice
	raw_id_fields = ['poll']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

	list_display = ['name' , 'question' , 'created' , 'total']
	search_fields = ['name' , 'created']
	inlines = [ChoiceTabular]



admin.site.register(Choice)



@admin.register(UserVotes)
class UserVotesAdmin(admin.ModelAdmin):

	list_display = ['user' , 'poll', 'user_ip' , 'total']
