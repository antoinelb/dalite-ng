from courseflow.lti import create_consumer


def test_create_consumer():
    data = {
        "url": "http://127.0.0.1/lti",
        "username": "test",
        "course_id": None,
        "course_list": False,
    }
    consumer = create_consumer(**data)

    data_ = consumer.generate_launch_data()
    assert data_["custom_course_id"] == ""
    assert data_["custom_course_list"] == "0"
    assert data_["user_id"] == data["username"]


def test_create_consumer__course_id():
    data = {
        "url": "http://127.0.0.1/lti",
        "username": "test",
        "course_id": 0,
        "course_list": False,
    }
    consumer = create_consumer(**data)

    data_ = consumer.generate_launch_data()
    assert data_["custom_course_id"] == "0"
    assert data_["custom_course_list"] == "0"
    assert data_["user_id"] == data["username"]


def test_create_consumer__course_list():
    data = {
        "url": "http://127.0.0.1/lti",
        "username": "test",
        "course_id": None,
        "course_list": True,
    }
    consumer = create_consumer(**data)

    data_ = consumer.generate_launch_data()
    assert data_["custom_course_id"] == ""
    assert data_["custom_course_list"] == "1"
    assert data_["user_id"] == data["username"]
