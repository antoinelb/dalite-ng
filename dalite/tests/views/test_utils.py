import json

from django.http import HttpResponse

from dalite.views.utils import (
    get_json_params,
    get_query_string_params,
    with_json_params,
    with_query_string_params,
)


def test_get_json_params(rf):
    data = {"arg1": 1, "arg2": 2, "opt_arg1": 3, "opt_arg2": 4}

    req = rf.post("/test", json.dumps(data), content_type="application/json")

    args = get_json_params(
        req,
        args=["arg1", "arg2"],
        opt_args=["opt_arg1", "opt_arg2", "opt_arg3"],
    )
    assert not isinstance(args, HttpResponse)
    args, opt_args = args

    assert data["arg1"] == args[0]
    assert data["arg2"] == args[1]
    assert data["opt_arg1"] == opt_args[0]
    assert data["opt_arg2"] == opt_args[1]
    assert opt_args[2] is None


def test_get_json_params__wrong_data(rf):
    data = {"arg1": 1, "arg2": 2}

    req = rf.post("/test", data)

    args = get_json_params(req, args=["arg1", "arg2"])
    assert isinstance(args, HttpResponse)


def test_get_json_params__missing_arg(rf):
    data = {"arg1": 1}

    req = rf.post("/test", json.dumps(data), content_type="application/json")

    args = get_json_params(req, args=["arg1", "arg2"])
    assert isinstance(args, HttpResponse)


def test_get_json_params(mocker):
    data = {"a": 1, "b": 2, "c": 3, "d": 4}

    req = mocker.Mock()
    req.body = json.dumps(data)

    args = get_json_params(req, args=["a", "b"], opt_args=["c", "d", "e"])

    assert not isinstance(args, HttpResponse)
    assert args[0] == [1, 2]
    assert args[1] == [3, 4, None]


def test_get_json_params__no_args(mocker):
    data = {}

    req = mocker.Mock()
    req.body = json.dumps(data)

    args = get_json_params(req)

    assert not isinstance(args, HttpResponse)
    assert args[0] == []
    assert args[1] == []


def test_get_json_params__wrong_type(mocker):
    req = mocker.Mock()
    req.body = "test"

    args = get_json_params(req)

    assert isinstance(args, HttpResponse)
    assert "Wrong data type was sent." in args.rendered_content


def test_get_json_params__missing_args(mocker):
    data = {"a": 1}

    req = mocker.Mock()
    req.body = json.dumps(data)

    args = get_json_params(req, args=["a", "b"])

    assert isinstance(args, HttpResponse)
    assert "There are missing parameters." in args.rendered_content


def test_get_query_string_params(mocker):
    data = {"a": 1, "b": 2, "c": 3, "d": 4}

    req = mocker.Mock()
    req.GET = data

    args = get_query_string_params(
        req, args=["a", "b"], opt_args=["c", "d", "e"]
    )

    assert not isinstance(args, HttpResponse)
    assert args[0] == [1, 2]
    assert args[1] == [3, 4, None]


def test_get_query_string_params__no_args(mocker):
    data = {}

    req = mocker.Mock()
    req.GET = data

    args = get_query_string_params(req)

    assert not isinstance(args, HttpResponse)
    assert args[0] == []
    assert args[1] == []


def test_get_query_string_params__missing_args(mocker):
    data = {"a": 1}

    req = mocker.Mock()
    req.GET = data

    args = get_query_string_params(req, args=["a", "b"])

    assert isinstance(args, HttpResponse)
    assert "There are missing parameters." in args.rendered_content


def test_with_json_params(mocker):
    get_json_params = mocker.patch(
        "dalite.views.utils.get_json_params", return_value=([1, 2, 3], [4, 5])
    )

    def test(req, a, b, c, d=None, e=None):  # pylint: disable=unused-argument
        return None

    decorator = with_json_params(args=["a", "b", "c"], opt_args=["d", "e"])
    fct = decorator(test)
    resp = fct(None)
    assert resp is None
    assert get_json_params.called_once()


def test_with_json_params__missing_params(mocker):
    get_json_params = mocker.patch(
        "dalite.views.utils.get_json_params", return_value=HttpResponse("test")
    )

    def test(req, a, b, c, d=None, e=None):  # pylint: disable=unused-argument
        return None

    decorator = with_json_params(args=["a", "b", "c"], opt_args=["d", "e"])
    fct = decorator(test)
    resp = fct(None)
    assert isinstance(resp, HttpResponse)
    assert get_json_params.called_once()


def test_with_query_string_params(mocker):
    get_query_string_params = mocker.patch(
        "dalite.views.utils.get_query_string_params",
        return_value=([1, 2, 3], [4, 5]),
    )

    def test(req, a, b, c, d=None, e=None):  # pylint: disable=unused-argument
        return None

    decorator = with_query_string_params(
        args=["a", "b", "c"], opt_args=["d", "e"]
    )
    fct = decorator(test)
    resp = fct(None)
    assert resp is None
    assert get_query_string_params.called_once()


def test_with_query_string_params__missing_params(mocker):
    get_query_string_params = mocker.patch(
        "dalite.views.utils.get_query_string_params",
        return_value=HttpResponse("test"),
    )

    def test(req, a, b, c, d=None, e=None):  # pylint: disable=unused-argument
        return None

    decorator = with_query_string_params(
        args=["a", "b", "c"], opt_args=["d", "e"]
    )
    fct = decorator(test)
    resp = fct(None)
    assert isinstance(resp, HttpResponse)
    assert get_query_string_params.called_once()
