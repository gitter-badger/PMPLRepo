from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
	if request.method == 'POST':
		return HTTPResponse(request.POST['item_text'])
	return render(request, 'home.html')
