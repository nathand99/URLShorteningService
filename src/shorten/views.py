from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import Url
from .forms import sumbit_url_form

from analytics.models import analytics

# Create your views here.
# 2 views that do the same thing
# function based view - handles all requests methods in this function eg get, post ...
# handles url - when user goes to url (with a shortened code) - we go to this function
# shortened is the varaible taken from the url (see urls.py)
# it is a kwarg. If we didnt include the shortened=None, it would turn up in kwargs
def redirect_view_function(request, shortened=None, *args, **kwargs):
    #obj = Url.objects.get(shortened=shortened)
    # get the object with given shortened. If doesnt exist - raise 404
    obj = get_object_or_404(Url, shortened=shortened)
    obj_url = obj.url
    print(obj_url)
    # must be a legit url eg https://www.google.com/
    # if its not, the it will append the url onto the current url
    return HttpResponseRedirect(obj_url)
    #return HttpResponse(f"Hello {obj_url}")


# class based view - each different request (get, post), get handled by a different method
# class based more portable - but more code
class url_redirect_view_class(View):
    def get(self, request, shortened=None, *args, **kwargs):
        # save item
        obj = get_object_or_404(Url, shortened=shortened)
        obj_url = obj.url
        analytics.objects.create_event(obj)
        return HttpResponseRedirect(obj_url)

def test_view(request, shortened=None, *args, **kwargs):
    return HttpResponse(f"Hello about")


class home_view(View):
    def get(self, request, *args, **kwargs):
        form = sumbit_url_form()
        context = {
            "title": "URL shortening service",
            "form": form
        }
        return render(request, "shorten/home.html", context)

    def post(self, request, *args, **kwargs):
        d = {}
        # d['url'] - gives an error sime that key is not in the dict
        d.get('url', "default value") # try to get url - if diesnt exist return default value. default is none. This is better since theres no error
        print(request.POST.get('url'))  # request.POST gives a dict of stuff coming in. We want the url 
        form = sumbit_url_form(request.POST)
        template = "shorten/home.html"
        context = {
            "title": "URL Shortening Service",
            "form": form
        }
        if form.is_valid():
            print(form.cleaned_data)
            url = form.cleaned_data.get("url")
            if not "http" in url:
                url = "http://" + url
            obj, created = Url.objects.get_or_create(url=url)
            context = {
                "object": obj,
                "created": created
            }   
            if created:
                template = "shorten/success.html"
            else:
                template = "shorten/alreadyexists.html"
        
        return render(request, template, context)




""" Class HttpResponseRedirect works with three kind of urls:

(1) Fully qualified URL e.g, 'https://www.yahoo.com/search/'

(2) An absolute path with no domain e.g, '/search/'

(3) A relative path e.g, 'search/'

If your functions not returns Fully qualified URL then it might be possible reason for appending url to existing url.

Please refer the Django official documentation for more information: https://docs.djangoproject.com/en/3.0/ref/request-response/ """