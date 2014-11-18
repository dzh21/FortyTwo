from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tasks42.models import Person, RequestObject
from tasks42.forms import PersonForm


def index(request):
    context = {'persons': Person.objects.all()}
    return render(request, "home.html", context)


def requests(request):
    context = {'requests': list(RequestObject.objects.all())[:10]}
    return render(request, "requests.html", context)


@login_required
def editcontacts(request):
    person = Person.objects.get(pk=1)
    context = {}

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            ob = form.save()
            resize_photo(ob.photo)
            return HttpResponseRedirect('/')
    else:
        form = PersonForm(instance=person)
        context = {'edit_person_form': form}

    return render(request, "editcontacts.html", context)


def resize_photo(img):
    from PIL import Image
    from django.conf import settings

    image = Image.open(settings.MEDIA_ROOT + '/' + str(img))

    image.thumbnail((200, 200), Image.ANTIALIAS)

    image.save(settings.MEDIA_ROOT + '/' + str(img), "JPEG")