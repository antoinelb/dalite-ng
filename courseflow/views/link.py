from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .decorators import teacher_required


@teacher_required
def link_page(req: HttpRequest) -> HttpResponse:
    """
    Returns the page where a teacher can link their courseflow account.

    Parameters
    ----------
    req : HttpRequest
        Request

    Returns
    -------
    HttpResponse
        The rendered page
    """
    return render(req, "courseflow/link.html")
