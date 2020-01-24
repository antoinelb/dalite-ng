from django import apps
from django.utils.translation import ugettext_lazy as translate


class CourseflowConfig(apps.AppConfig):
    name = "courseflow"
    verbose_name = translate("CourseFlow integration")
