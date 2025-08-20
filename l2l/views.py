from datetime import datetime

from django.http import HttpResponse
from django.template import loader


def index(request):
    now = datetime.now()
    template = loader.get_template("l2l/index.html")
    context = {"iso": now.strftime("%Y-%m-%dT%H:%M:%S"), "now": now}
    return HttpResponse(template.render(context, request))
