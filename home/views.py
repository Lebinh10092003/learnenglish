from django.shortcuts import render

# Create your views here.
def home(request):
    request.session['current_page'] = 'home'
    return render(request, 'home.html')
