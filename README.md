# Using Behave (Gherkin) to Test RBAC Service

The goal of this POC is to demonstrate how one would use Behave to take a BDD
approach to testing the API provided by the RBAC service. Existing tests take a 
primarily procedural approach to building testing automation. 

## Why??

Our current approach has the following drawbacks:

1. Typically by the time a feature is being tested/automated, it has already gone through the development pipeline and 
been chucked over the fence. By this time it is typically too late to consider the experience of the user. Any 
corrections made at this point are typically functional in nature and will not address the user experience of the API consumer.
2. When it comes to defining the capabilities of our APIs, this is often left to primarily technical users. While this 
may be adequate, it leaves us blind to the sometimes myopic view of the engineers that have been staring at the problem for far too long.

With a BDD approach, we may have the following benefits:

1. A "spec first" or "behavior first" approach to defining new functionality.
2. An easily-shared definition (the feature file) that can be reviewed by both technical and non-technical stakeholders.

## Shortcomings

Behave feels somewhat incomplete; it lacks polish around the edges when compared to other languages that support 
Gherkin, such as Java.

## Side Benefits

* Behave is supported in PyCharm Professional edition and partially supported in VSCode.

## Running the Tests

Pre-requisites: You need python and tox installed on your system.

### Configuring tests

You'll want to define the required environment variables needed to configure the tests. Something like this should do.

```bash
export RBAC_ORG_USER=iqe_rbac_admin
export RBAC_ORG_PASSWORD=<REDACTED>
export RBAC_SERVICE_HOSTNAME=https://ci.cloud.redhat.com
export RBAC_URL_SUFFIX=/api/rbac/v1/
export RBAC_NORMAL_USER=iqe_normal_user
export RBAC_NORMAL_PASSWORD=<REDACTED>                                          
```

If you don't want to type these every time, simply slap those statements in a shell script and source it before you run the tests. Like this:

`source ci_env.sh`

Once you've configured the environment variables, you're ready to run the tests.

### Executing Tests

There are two relatively easy ways to run the tests. 

Option 1. Use behave directly

   1. Create a virtual environment
    `virtualenv env`
   2. Activate the virtual environment
    `source env/bin/activate`
   3. Install dependencies
    `pip install -r requirements.txt`
   4. Run behave
    `behave`

Option 2. Use tox

The provided tox file will set up the environment and execute the tests for you.

1. `tox -re dev`

### Example Output

```text
Feature: Obtain details about groups known to the RBAC service # features/groups.feature:1

  Scenario: Get the set of principals as an org admin         # features/groups.feature:3
    Given the RBAC service is running                         # features/steps/status.py:7 0.000s
    And the current user is an org administrator              # features/steps/principals.py:47 0.000s
    When a request is made to obtain principal information    # features/steps/principals.py:9 2.833s
    Then the RBAC service returns the set of known principals # features/steps/principals.py:20 0.000s

  Scenario: Get the set of principals as a non-org-admin         # features/groups.feature:10
    Given the RBAC service is running                            # features/steps/status.py:7 0.000s
    And the current user is a non-administrator                  # features/steps/principals.py:57 0.000s
    When a request is made to obtain principal information       # features/steps/principals.py:9 2.015s
    Then the RBAC service indicates this operation is prohibited # features/steps/principals.py:39 0.000s

Feature: Obtain details about principals known to the service # features/principals.feature:1

  Scenario: Get the set of principals as an org admin         # features/principals.feature:3
    Given the RBAC service is running                         # features/steps/status.py:7 0.000s
    And the current user is an org administrator              # features/steps/principals.py:47 0.000s
    When a request is made to obtain principal information    # features/steps/principals.py:9 1.320s
    Then the RBAC service returns the set of known principals # features/steps/principals.py:20 0.000s

  Scenario: Get the set of principals as a non-org-admin         # features/principals.feature:10
    Given the RBAC service is running                            # features/steps/status.py:7 0.000s
    And the current user is a non-administrator                  # features/steps/principals.py:57 0.000s
    When a request is made to obtain principal information       # features/steps/principals.py:9 0.407s
    Then the RBAC service indicates this operation is prohibited # features/steps/principals.py:39 0.000s

Feature: Retrieve role information # features/roles.feature:1
  In order to manage user permissions, I want my organization administrator
  to be able to access the role information and non-administrators to be
  prohibited from doing so.
  Scenario: Organization Administrator                          # features/roles.feature:6
    Given a set of specific roles                               # features/steps/roles.py:26 1.928s
      | name        | description    |
      | BehaveRole1 | Beer Cans      |
      | BehaveRole2 | Silly Walks    |
      | BehaveRole3 | Anvil Dropping |
    When The role information is requested as Org Admin         # features/steps/roles.py:74 2.475s
    Then The role information matches the set of specific roles # features/steps/roles.py:89 0.001s
      | name        | description    |
      | BehaveRole1 | Beer Cans      |
      | BehaveRole2 | Silly Walks    |
      | BehaveRole3 | Anvil Dropping |
      Traceback (most recent call last):
        File "/home/reavis/hackathon/.tox/dev/lib/python3.8/site-packages/behave/model.py", line 1329, in run
          match.run(runner.context)
        File "/home/reavis/hackathon/.tox/dev/lib/python3.8/site-packages/behave/matchers.py", line 98, in run
          self.func(context, *args, **kwargs)
        File "features/steps/roles.py", line 103, in role_info_matches_specific_roles
          assert _exists_in_responses(context.responses, role_data)
        File "features/steps/roles.py", line 97, in _exists_in_responses
          if response.get("name") == row_data.get("name"):
      AttributeError: 'Response' object has no attribute 'get'


  Scenario: Normal User                                     # features/roles.feature:21
    When The role information is requested as a normal user # features/steps/roles.py:114 0.348s
    Then The response should indicate access is not allowed # features/steps/roles.py:106 0.000s

Feature: Obtain RBAC service status # features/status.feature:1

  Scenario: Basic Status Check when service is up  # features/status.feature:3
    Given the RBAC service is running              # features/steps/status.py:7 0.000s
    When A request is made to check the status     # features/steps/status.py:12 1.256s
    Then The service indicates it is operational   # features/steps/status.py:19 0.000s


Failing scenarios:
  features/roles.feature:6  Organization Administrator

3 features passed, 1 failed, 0 skipped
6 scenarios passed, 1 failed, 0 skipped
23 steps passed, 1 failed, 0 skipped, 0 undefined
Took 0m12.583s
ERROR: InvocationError for command /home/reavis/hackathon/.tox/dev/bin/behave (exited with code 1)
___________________________________________________________________________________________ summary ___________________________________________________________________________________________
ERROR:   dev: commands failed

```