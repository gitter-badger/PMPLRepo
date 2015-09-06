from django.http import HttpResponse

def home_page(request):
	return HttpResponse('<html><title>To-Do lists</title><body>Nama : Tyas Kusuma H<br>NPM : 1206208214</body></html>')
