from typing import Optional

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_safe

from dalite.views.utils import with_json_params, with_query_string_params

from ..lti import create_consumer


@require_safe
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
        return courseflow(req)
    else:
        return render(req, "courseflow/login.html")


@require_POST
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


@require_safe
@with_query_string_params(opt_args=["course_id"])
def courseflow(
    req: HttpRequest, course_id: Optional[str] = None
) -> HttpResponse:
    """
    Redirects to CourseFlow lti using the username and email from the
    `req.user`.

    Parameters
    ----------
    req : HttpRequest
        Request with possibly a User attacher
    course_id : Optional[str] (default : None)
        If this should lead to a specific course on courseflow

    Returns
    -------
    HttpResponse
        The lti page that will redirect to courseflow
        The redirected respones to COURSEFLOW_URL/lti
    """
    url = f"{settings.COURSEFLOW_URL}/lti/"
    if not url.startswith("http"):
        url = f"http://{url}"
    consumer = create_consumer(url, course_id=course_id)
    return render(
        req,
        "courseflow/lti.html",
        {
            "launch_url": consumer.launch_url,
            "launch_data": consumer.generate_launch_data(),
        },
    )
