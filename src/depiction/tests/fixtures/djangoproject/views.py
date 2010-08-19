from django.http import HttpResponse

def dummy_view(request):
    return HttpResponse('You ran a test.')
