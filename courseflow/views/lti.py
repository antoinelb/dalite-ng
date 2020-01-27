from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from dalite.views.utils import with_json_params


def login(req: HttpRequest) -> HttpResponse:
    """
    Page for dalite user to login, redirects directly to CourseFlow lti. If the
    user was already logged in, redirects directly to CourseFlow. If not,
    returns a page where they can enter their credentials.

    Parameters
    ----------
    req : HttpRequest
        Request with possibly a User attacher

    Returns
    -------
    HttpResponse
        Either a rendered page or a redirect to the given `redirect`
    """
    if isinstance(req.user, User):
        return redirect(req)
    else:
        return render(req, "courseflow/login.html")


@with_json_params(args=["username", "password"])
def authenticate(
    req: HttpRequest, username: str, password: str
) -> HttpResponse:
    """
    Authenticates the student or returns an error message.

    Parameters
    ----------
    req : HttpRequest
        Request
    username : str
        Username
    password : str
        Password

    Returns
    -------
    HttpResponse
        Either an 401 response or a 200 one
    """
    user = auth.authenticate(req, username=username, password=password)
    if user is None:
        return HttpResponse(
            "Either the username or password are wrong.",
            content_type="text/plain",
            status=401,
        )
    else:
        auth.login(req, user)
        return HttpResponse("")


def redirect(req: HttpRequest) -> HttpResponse:
    """
    Redirects to CourseFlow lti using the username and email from the
    `req.user`.

    Parameters
    ----------
    req : HttpRequest
        Request with possibly a User attacher

    Returns
    -------
    HttpResponse
        The redirected respones to COURSEFLOW_URL/lti
    """
    url = settings.COURSEFLOW_URL
    return HttpResponse("localhost:3000/teacher/dashboard")
