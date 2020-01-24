from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from django.shortcuts import render


@login_required
def index(req: HttpRequest) -> HttpResponse:
    courseflow_url = "https://wfm.saltise.ca/CourseFlow/courseplanner.html"
    context = {"courseflow_url": courseflow_url}
    return render(req, "courseflow/index.html", context)
