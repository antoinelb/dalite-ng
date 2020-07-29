import os

import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.forms import model_to_dict

from peerinst.models import (
    Answer,
    Student,
    StudentGroup,
    StudentGroupMembership,
    Teacher,
)
from tos.models import Consent


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("[*] Getting students with consent...", end="\r")
        students = get_students_with_consent()[
            ["id", "username"]
        ].drop_duplicates()
        print("[+] Got students with consent.".ljust(80))

        print("[*] Getting student group memberships...", end="\r")
        memberships = get_student_group_memberships(students)
        print("[+] Got student group memberships.".ljust(80))

        print("[*] Combining group memberships to answers...", end="\r")
        answers = combine_answers_with_group_membership(memberships)
        print("[+] Combined group memberships to answers.".ljust(80))

        print("[*] Saving data...", end="\r")
        answers.to_csv(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                os.pardir,
                "answer_groups.csv",
            ),
            index=False,
        )
        print("[+] Saved data.".ljust(80))


def get_students_with_consent() -> pd.DataFrame:
    users = pd.DataFrame(User.objects.values())
    students = pd.DataFrame(Student.objects.values())
    consents = pd.DataFrame(
        Consent.objects.filter(
            tos__role__role="student", accepted=True
        ).values()
    )[["user_id"]]
    return (
        pd.merge(
            pd.merge(
                students, consents, left_on="student_id", right_on="user_id"
            ),
            users,
            left_on="user_id",
            right_on="id",
        )
        .drop(columns="id_y")
        .rename(columns={"id_x": "id"})
    )


def get_student_group_memberships(students: pd.DataFrame) -> pd.DataFrame:
    memberships = pd.DataFrame(StudentGroupMembership.objects.values())[
        ["student_id", "group_id"]
    ]
    groups_ = [model_to_dict(g) for g in StudentGroup.objects.all()]
    groups = pd.DataFrame(
        [
            {
                **group,
                **{
                    "teacher": [
                        teacher.user.username for teacher in group["teacher"]
                    ]
                },
            }
            for group in groups_
        ]
    )[["id", "name", "title", "teacher"]]
    memberships = pd.merge(
        memberships, groups, left_on="group_id", right_on="id"
    )[["student_id", "name", "title", "teacher"]]
    memberships.head()
    return pd.merge(
        students, memberships, left_on="id", right_on="student_id"
    )[["username", "name", "title", "teacher"]].rename(
        columns={
            "name": "group_name",
            "title": "group_title",
            "teacher": "teachers",
        }
    )


def combine_answers_with_group_membership(
    memberships: pd.DataFrame,
) -> pd.DataFrame:
    answers = pd.DataFrame(Answer.objects.values())[["id", "user_token"]]
    return pd.merge(
        answers,
        memberships,
        left_on="user_token",
        right_on="username",
        how="left",
    ).drop(columns="user_token")
