from behave import *
from rbac_test_util.util_functions import (
    create_role,
    delete_role,
    get_roles,
    get_role_with_access,
)

from features.environment import admin_user, normal_user

use_step_matcher("re")


def before_scenario(context, feature):
    pass


def after_scenario(context, feature):
    admin_user_cred = use_fixture(admin_user, context)
    for row in context.table:
        username = admin_user_cred["username"]
        password = admin_user_cred["password"]
        delete_role(username, password, row["name"])


@given("a set of specific roles")
def a_set_of_specific_roles(context):
    """
    :type context: behave.runner.Context
    """

    def _role_exists(role_name):
        admin_cred = use_fixture(admin_user, context)
        response = get_roles(
            admin_cred["username"], admin_cred["password"], name=role_name
        )
        if response.status_code == 200 and response.json().get("meta").get("count") > 0:
            return True, response.json().get("data")[0].get("uuid")
        else:
            return False

    context.role_data = []
    for row in context.table:
        # check if role exists
        role_exists = _role_exists(row["name"])
        if role_exists is not False:
            # if it does, skip creation
            context.role_data.append(role_exists[1])
            continue

        # otherwise create the role data
        role_data = {
            "name": row["name"],
            "description": row["description"],
            "access": [
                {
                    "permission": "cost-management:*:read",
                    "resourceDefinitions": [
                        {
                            "attributeFilter": {
                                "key": "cost-management.aws.account",
                                "operation": "equal",
                                "value": "123456",
                            }
                        }
                    ],
                }
            ],
        }
        new_role_uuid = create_role(role_data)
        context.role_data.append(new_role_uuid)


@when("The role information is requested as Org Admin")
def role_information_is_requested_as_org_admin(context):
    """
    :type context: behave.runner.Context
    """
    admin_cred = use_fixture(admin_user, context)
    context.responses = []
    for role_response in context.role_data:
        response = get_role_with_access(
            role_response, admin_cred["username"], admin_cred["password"]
        )
        assert response.status_code == 200, str(response.status_code)
        context.responses.append(response)


@then("The role information matches the set of specific roles")
def role_info_matches_specific_roles(context):
    """
    :type context: behave.runner.Context
    """

    def _exists_in_responses(responses, row_data):
        for response in responses:
            if response.get("name") == row_data.get("name"):
                return True
        return False

    for row in context.table:
        role_data = {"name": row["name"], "description": row["description"]}
        assert _exists_in_responses(context.responses, role_data)


@then("The response should indicate access is not allowed")
def response_indicates_access_is_not_allowed(context):
    """
    :type context: behave.runner.Context
    """
    assert context.response.status_code == 403


@when("The role information is requested as a normal user")
def role_information_is_requested_as_normal_user(context):
    """
    :type context: behave.runner.Context
    """
    normal_cred = use_fixture(normal_user, context)
    response = get_roles(normal_cred["username"], normal_cred["password"])
    context.response = response
