from vans.models import Van

def vans(request):
	return {
		'vans': Van.objects.all().values('id', 'slug', 'name')
	}