from django.shortcuts import render , get_object_or_404
from polls.models import Poll
from .fusioncharts import FusionCharts



def chart(request , poll_id , poll_slug):

	poll = get_object_or_404(Poll , id=poll_id , slug=poll_slug , total__gte=1)

	dataSource = {}

	chartConfig = {}


	chartConfig["caption"] = poll.name + " results"
	chartConfig["subCaption"] = poll.question
	chartConfig["xAxisName"] = None
	chartConfig["yAxisName"] = "Votes"
	chartConfig["numberSuffix"] = " persons"
	chartConfig["theme"] = "fusion"

	dataSource["chart"] = chartConfig

	dataSource["data"] = []

	choices = poll.choices.all()

	for choice in choices:

		dataSource["data"].append({"label":choice.field , "value":choice.total})


	column2D = FusionCharts("column2d" , "myFirstChart" , "600" , "400" , "myFirstChart-container" , "json" , dataSource)


	return render(request , 'chart.html' , {'output':column2D.render(),
											'poll':poll})


