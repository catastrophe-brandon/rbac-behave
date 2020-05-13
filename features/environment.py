from behave import fixture
import os
import requests


@fixture
def admin_user(context, *args, **kwargs):
    credential = {
        "username": os.environ["RBAC_ORG_USER"],
        "password": os.environ["RBAC_ORG_PASSWORD"],
    }
    return credential


@fixture
def normal_user(context, *args, **kwargs):
    credential = {
        "username": os.environ["RBAC_NORMAL_USER"],
        "password": os.environ["RBAC_NORMAL_PASSWORD"],
    }
    return credential


@fixture
def rbac_client(context, environment, user):
    """

    :param context:
    :param environment:
    :param user:
    :return:
    """
    session = requests.Session()
