from behave import *
from rbac_test_util.group_functions import get_groups

use_step_matcher("re")


@when("a request is made to obtain group information")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.group_response = get_groups(
        context.current_username, context.current_password
    )


@then("the RBAC service returns the set of known groups")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.group_response.status_code == 200
