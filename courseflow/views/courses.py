from dalite.views.utils import with_json_params


from django.http import HttpRequest, HttpResponse


def get_courseflow_courses(req: HttpRequest) -> HttpResponse:
    """
    Gets the list of courseflow courses.
    """


@with_json_params(args=["group_id"])
def update_linked_course(req: HttpRequest, group_id: int) -> HttpResponse:
    """
    Updates which course is linked to the `group_id`.
    """
