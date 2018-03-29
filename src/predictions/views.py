from django.shortcuts import render
from django.views.generic import ListView


from .models import get_tweets

class SearchTwitterView(ListView):

	template_name = "predictions/search-twitter.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchTwitterView, self).get_context_data(*args, **kwargs)
		method_dict = self.request.GET
		query = method_dict.get('content', None) # method_dict['q']
		if query is not None:
			print(query)
			context= {}
			context['tweets'] = get_tweets(str(query))
			return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dict = request.GET
		query = method_dict.get('content', None) # method_dict['q']
		if query is not None:
			print(query)
			context= {}
			context['tweets'] = get_tweets(str(query))
			return context


