from typing import Optional

from django.conf import settings

from lti import ToolConsumer


def create_consumer(
    url: str, course_id: Optional[int] = None, course_list: bool = False
) -> ToolConsumer:
    consumer = ToolConsumer(
        consumer_key=settings.LTI_CLIENT_KEY,
        consumer_secret=settings.LTI_CLIENT_SECRET,
        launch_url=url,
        params={
            "lti_message_type": "basic-lti-launch-request",
            "lti_version": "1.0",
            "resource_link_id": "0",
            "context_id": "test",
            "context_title": "test",
            "custom_course_id": str(course_id)
            if course_id is not None
            else "",
            "custom_course_list": "1" if course_list else "0",
            "lis_outcome_service_url": url,
            "lis_result_sourcedid": url,
            "roles": "Learner",
            "user_id": "YW50b2luZWxi",
        },
    )

    return consumer
