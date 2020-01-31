from django.contrib import auth
from django.http import HttpResponse
from django.urls import reverse

from peerinst.students import get_student_username_and_password


def test_login(client):
    resp = client.get(reverse("courseflow:login"))

    assert isinstance(resp, HttpResponse)
    assert "courseflow/login.html" in [t.name for t in resp.templates]


def test_login__logged_in(client, user, mocker):
    client.login(username=user.username, password="test")

    courseflow = mocker.patch(
        "courseflow.views.lti.courseflow",
        return_value=HttpResponse("__test__"),
    )

    resp = client.get(reverse("courseflow:login"))
    courseflow.assert_called_once()
    assert "__test__" in resp.content.decode()


def test_authenticate(client, user):
    resp = client.post(
        reverse("courseflow:authenticate"),
        {"username": user.username, "password": "test"},
        content_type="application/json",
    )
    assert auth.get_user(client).is_authenticated


def test_authenticate__wrong_credentials(client, user):
    resp = client.post(
        reverse("courseflow:authenticate"),
        {"username": user.username, "password": "wrong"},
        content_type="application/json",
    )
    assert (
        resp.content.decode() == "Either the username or password are wrong."
    )
    assert resp.status_code == 401
    assert not auth.get_user(client).is_authenticated


def test_courseflow(client, teacher):
    client.login(username=teacher.user.username, password="test")

    resp = client.get(reverse("courseflow:courseflow"),)
    assert "courseflow/lti.html" in [t.name for t in resp.templates]

    content = resp.content.decode()
    assert (
        "<input "
        'name="custom_course_id" '
        'type="hidden" '
        'value=""/>' in content
    )
    assert (
        "<input "
        'name="custom_course_list" '
        'type="hidden" '
        'value="0"/>' in content
    )
    assert (
        "<input "
        'name="user_id" '
        'type="hidden" '
        f'value="{teacher.user.username}"/>' in content
    )


def test_courseflow__course_id(client, teacher):
    client.login(username=teacher.user.username, password="test")

    resp = client.get(f"{reverse('courseflow:courseflow')}?course_id=0")
    assert "courseflow/lti.html" in [t.name for t in resp.templates]

    content = resp.content.decode()
    assert (
        "<input "
        'name="custom_course_id" '
        'type="hidden" '
        'value="0"/>' in content
    )
    assert (
        "<input "
        'name="custom_course_list" '
        'type="hidden" '
        'value="0"/>' in content
    )
    assert (
        "<input "
        'name="user_id" '
        'type="hidden" '
        f'value="{teacher.user.username}"/>' in content
    )


def test_courseflow__not_logged_in(client, student):
    resp = client.get(reverse("courseflow:courseflow"),)
    assert resp.status_code == 403


def test_courseflow__no_teacher_access(client, student):
    username, password = get_student_username_and_password(
        student.student.email
    )
    client.login(username=username, password=password)

    resp = client.get(reverse("courseflow:courseflow"),)
    assert resp.status_code == 403
