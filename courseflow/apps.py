from django import apps  # pragma: no cover
from django.utils.translation import (
    ugettext_lazy as translate,
)  # pragma: no cover


class CourseflowConfig(apps.AppConfig):  # pragma: no cover
    name = "courseflow"
    verbose_name = translate("CourseFlow integration")
