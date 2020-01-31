from django.urls import reverse
from django.contrib import auth
from django.http import HttpResponse


def test_login(client):
    resp = client.get(reverse("courseflow:login"))

    assert isinstance(resp, HttpResponse)
    assert "courseflow/login.html" in [t.name for t in resp.templates]


def test_login__logged_in(client, user, mocker):
    client.login(username=user.username, password="test")

    redirect = mocker.patch(
        "courseflow.views.redirect", return_value=HttpResponse("__test__")
    )

    resp = client.get(reverse("courseflow:login"))
    redirect.assert_called_once()
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