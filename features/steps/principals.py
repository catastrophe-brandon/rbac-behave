from behave import *
from rbac_test_util.util_functions import get_principals

from features.environment import admin_user, normal_user

use_step_matcher("re")


@when("a request is made to obtain principal information")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    principal_response = get_principals(
        context.current_username, context.current_password
    )
    context.response = principal_response


@then("the RBAC service returns the set of known principals")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.response.status_code == 200
    # TODO: Verify that all the data in the response is sane


@when("a request is made to obtain principal information as a normal user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u"STEP: When a request is made to obtain principal information as a normal user"
    )


@then("the RBAC service indicates this operation is prohibited")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.response.status_code == 403


@step("the current user is an org administrator")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    org_administrator_creds = use_fixture(admin_user, context)
    context.current_username = org_administrator_creds["username"]
    context.current_password = org_administrator_creds["password"]


@step("the current user is a non-administrator")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    user_creds = use_fixture(normal_user, context)
    context.current_username = user_creds["username"]
    context.current_password = user_creds["password"]
