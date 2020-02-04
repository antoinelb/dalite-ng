from django.urls import reverse

from .fixtures import create_consumer


def test_lti(client, rf):
    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri()
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 302
    assert resp.url == "/en/assignment/test/0/"


def test_lti__wrong_key_or_secret(client, rf, caplog):
    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(), secret="wrong"
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "There was an error with either the client key or secret. "
        "You may verify that secret hasn't changed on your account "
        'at <a href="https://mydalite.org">https://mydalite.org</a> '
        "or alert your teacher."
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made with an error on either the key or secret."
    )


def test_lti__missing_params(client, rf, caplog):
    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={
            "custom_question_id": "0",
            "custom_teacher_id": "test",
            "user_id": "test",
        },
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "The following parameter is missing in your settings:<br/>"
        + "\xa0\xa0 - custom_assignment_id"
        + "<br/>You can find them on your account page on "
        '<a href="https://mydalite.org">https://mydalite.org</a>.'
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made with the missing parameter "
        "`custom_assignment_id`"
    )
    caplog.clear()

    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={
            "custom_assignment_id": "test",
            "custom_teacher_id": "test",
            "user_id": "test",
        },
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "The following parameter is missing in your settings:<br/>"
        + "\xa0\xa0 - custom_question_id"
        + "<br/>You can find them on your account page on "
        '<a href="https://mydalite.org">https://mydalite.org</a>.'
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made with the missing parameter "
        "`custom_question_id`"
    )
    caplog.clear()

    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={
            "custom_assignment_id": "test",
            "custom_question_id": "0",
            "user_id": "test",
        },
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "The following parameter is missing in your settings:<br/>"
        + "\xa0\xa0 - custom_teacher_id"
        + "<br/>You can find them on your account page on "
        '<a href="https://mydalite.org">https://mydalite.org</a>.'
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made with the missing parameter "
        "`custom_teacher_id`"
    )
    caplog.clear()

    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={"user_id": "test"},
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "The following parameter is missing in your settings:<br/>"
        + "\xa0\xa0 - custom_assignment_id"
        + "<br/>You can find them on your account page on "
        '<a href="https://mydalite.org">https://mydalite.org</a>.'
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made with the missing parameter "
        "`custom_assignment_id`"
    )


def test_lti__missing_oauth(client, rf, caplog):
    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={"custom_question_id": "0", "custom_teacher_id": "test"},
    )
    resp = client.post(reverse("lti:lti"))
    assert resp.status_code == 400
    assert (
        "You can't access this url directly. Please go through "
        '<a href="https://mydalite.org">https://mydalite.org</a> or the link '
        "on your class website."
    ) in resp.content.decode()
    assert (
        next(
            record for record in caplog.records if record.name == "lti"
        ).getMessage()
        == "A direct lti access was tried"
    )


def test_lti__missing_user_id(client, rf, caplog):
    consumer = create_consumer(
        rf.post(reverse("lti:lti")).build_absolute_uri(),
        params={
            "custom_assignment_id": "test",
            "custom_question_id": "0",
            "custom_teacher_id": "test",
        },
    )
    resp = client.post(consumer.launch_url, consumer.generate_launch_data())
    assert resp.status_code == 400
    assert (
        "Your lti application isn't sending a needed parameter. "
        "Please contact myDalite support at support@scivero.com."
    ) in resp.content.decode()
    assert next(
        record for record in caplog.records if record.name == "lti"
    ).getMessage() == (
        "An lti request was made from an application not sending "
        "the `user_id` parameter."
    )
