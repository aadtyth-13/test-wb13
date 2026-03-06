from django.shortcuts import render

def home(request):
    return render(request, 'page/home.html', {'active': 'home'})

def blog(request):
    return render(request, 'page/blog.html', {'active': 'blog'})

def product(request):
    return render(request, 'page/product.html', {'active': 'product'})

def event(request):
    return render(request, 'page/event.html', {'active': 'event'})

def request(request):
    return render(request, 'page/request.html', {'active': 'request'})

def information(request):
    return render(request, 'page/information.html', {'active': 'information'})

def version(request):
    return render(request, 'page/version.html', {'active': 'version'})