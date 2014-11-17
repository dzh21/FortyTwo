from django.shortcuts import render
from django.http import HttpResponseRedirect
from tasks42.models import Person, RequestObject
from tasks42.forms import PersonForm


def index(request):
    context = {'persons': Person.objects.all()}
    return render(request, "home.html", context)


def requests(request):
    context = {'requests': list(RequestObject.objects.all())[:10]}
    return render(request, "requests.html", context)


def editcontacts(request):
    person = Person.objects.get(pk=1)
    context = {}

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PersonForm(instance=person)
        context = {'edit_person_form': form}

    return render(request, "editcontacts.html", context)