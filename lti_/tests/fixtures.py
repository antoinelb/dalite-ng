from typing import Dict, Optional

from django.conf import settings
from lti import ToolConsumer


def create_consumer(
    url: str,
    secret: Optional[str] = None,
    params: Optional[Dict[str, str]] = None,
) -> ToolConsumer:
    if secret is None:
        secret = settings.LTI_CLIENT_SECRET
    if params is None:
        params = {
            "custom_assignment_id": "test",
            "custom_question_id": "0",
            "custom_teacher_id": "test",
            "user_id": "test",
        }
    consumer = ToolConsumer(
        consumer_key=settings.LTI_CLIENT_KEY,
        consumer_secret=secret,
        launch_url=url,
        params={
            **{
                "lti_message_type": "basic-lti-launch-request",
                "lti_version": "1.0",
                "resource_link_id": "0",
                "context_id": "test",
                "context_title": "test",
                "lis_outcome_service_url": url,
                "lis_result_sourcedid": url,
                "roles": "Learner",
            },
            **params,
        },
    )

    return consumer
