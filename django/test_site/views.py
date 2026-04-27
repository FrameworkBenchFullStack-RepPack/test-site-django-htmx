import asyncio
from django.http import StreamingHttpResponse
from .live import async_clients, start_live_broadcast
from django.shortcuts import render
from .forms import PeopleForm
from .middleware import no_compress
from models.models import Category, Person


def home(request):
    form_defaults = {**PeopleForm.DEFAULTS, "size": 8}
    if request.GET:
        form = PeopleForm(request.GET, initial=form_defaults)
    else:
        form = PeopleForm(initial=form_defaults)
    params = {**form_defaults, **{k: v for k, v in (form.cleaned_data.items() if form.is_valid() else {}.items()) if v is not None}}

    categories = Category.objects.order_by('name')
    people = Person.objects.filtered(**params)

    if request.headers.get("HX-Request") and not request.headers.get("HX-Boosted"):
        return render(request, "partials/list/list_content.html", { "people": people })

    return render(request, "home/index.html", { "form": form, "categories": categories, "people": people })


def static_1(request):
    return render(request, "static-1/index.html")

def static_2(request):
    return render(request, "static-2/index.html")

def live(request):
    return render(request, "live/index.html")

def list_view(request):
    form_defaults = {**PeopleForm.DEFAULTS, "size": 100}
    if request.GET:
        form = PeopleForm(request.GET, initial=form_defaults)
    else:
        form = PeopleForm(initial=form_defaults)
    params = {**form_defaults, **{k: v for k, v in (form.cleaned_data.items() if form.is_valid() else {}.items()) if v is not None}}

    categories = Category.objects.order_by('name')
    people = Person.objects.filtered(**params)

    if request.headers.get("HX-Request") and not request.headers.get("HX-Boosted"):
        return render(request, "partials/list/list_content.html", { "people": people })

    return render(request, "list/index.html", { "form": form, "categories": categories, "people": people })


@no_compress
async def live_stream(request):
    start_live_broadcast()
    queue = asyncio.Queue(maxsize=1)
    async_clients.append(queue)

    async def iter_queue():
        try:
            while True:
                yield await queue.get()
        finally:
            if queue in async_clients:
                async_clients.remove(queue)

    response = StreamingHttpResponse(iter_queue(), content_type="text/event-stream")
    response["Cache-Control"] = "no-store, no-cache"
    return response