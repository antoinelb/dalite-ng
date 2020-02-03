import logging

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext_lazy as translate
from django.views.decorators.csrf import csrf_exempt
from django_lti_tool_provider.views import LTIView
from lti.utils import InvalidLTIRequestError

from dalite.views.errors import response_400

logger = logging.getLogger("lti")


@csrf_exempt
def lti(req: HttpRequest) -> HttpResponse:
    link = '<a href="https://mydalite.org">https://mydalite.org</a>'
    try:
        resp = LTIView.as_view()(req)
    except InvalidLTIRequestError:
        return response_400(
            req,
            translate(
                "You can't access this url directly. Please go through "
                f"{link} or the link on your class website."
            ),
            "A direct access was tried",
            logger.warning,
        )
    except KeyError as e:
        return response_400(
            req,
            translate(
                "The following parameter is missing in your settings:<br>"
                + "<br>".join(f"&nbsp;&nbsp; - {arg}" for arg in e.args)
            ),
            f"An lti request was made with the missing parameter {e.args[0]}",
            logger.warning,
        )
    if resp.status_code == 400:
        return response_400(
            req,
            translate(
                "There was an error with either the client key or secret. "
                "You may verify that secret hasn't changed on your account "
                f"at {link} or alert your teacher."
            ),
            "An lti request was made with an error on either the key or "
            "secret.",
            logger.error,
        )
    return resp
