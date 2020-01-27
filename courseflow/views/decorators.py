import logging

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as translate

from dalite.views.errors import response_403
from peerinst.models import Teacher

logger = logging.getLogger("courseflow")


def teacher_required(fct):
    def wrapper(req, *args, **kwargs):
        if not isinstance(req.user, User):
            return response_403(
                req,
                msg=translate("You don't have access to this resource."),
                logger_msg=(
                    "Access to {} from a non teacher user.".format(req.path)
                ),
                log=logger.warning,
            )
        try:
            teacher = Teacher.objects.get(user=req.user)
            return fct(req, *args, teacher=teacher, **kwargs)
        except Teacher.DoesNotExist:
            return response_403(
                req,
                msg=translate("You don't have access to this resource."),
                logger_msg=(
                    "Access to {} from a non teacher user.".format(req.path)
                ),
                log=logger.warning,
            )

    return wrapper
