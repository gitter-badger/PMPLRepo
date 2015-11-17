from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
	return render(request, 'home.html', {'comment' : 'yey,waktunya libur'})

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	#items= Item.objects.filter(list=list_)
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'], list=list_)	
		return redirect('/lists/%d/' % (list_.id,))

	jumlah_item = Item.objects.filter(list=list_).count()
	str =''
	if jumlah_item == 0:
		str = 'yey,waktunya libur'
	elif jumlah_item < 5:
		str = 'sibuk, tapi santai'
	else:
		str = 'oh tidak'	

	return render(request, 'list.html', {'list': list_ , 'comment': str} )

def new_list(request):
	list_ = List.objects.create()
	item = Item(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect('/lists/%d/' % (list_.id,))

#def add_item(request, list_id):
#	list_ = List.objects.get(id=list_id)
#	Item.objects.create(text=request.POST['item_text'], list=list_)	
#	return redirect('/lists/%d/' % (list_.id,))
