from behave import given, when, then, use_fixture
from rbac_test_util.util_functions import get_status

from features.environment import normal_user


@given("the RBAC service is running")
def the_rbac_service_is_running(context):
    pass


@when("A request is made to check the status")
def status_request_made(context):
    normal_user_cred = use_fixture(normal_user, context)
    response = get_status(normal_user_cred["username"], normal_user_cred["password"])
    context.status_response = response


@then("The service indicates it is operational")
def the_service_is_operational(context):
    assert context.status_response.status_code == 200
