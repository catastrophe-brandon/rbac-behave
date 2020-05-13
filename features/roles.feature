Feature: Retrieve role information
	In order to manage user permissions, I want my organization administrator
    to be able to access the role information and non-administrators to be
    prohibited from doing so.

  Scenario: Organization Administrator
    Given a set of specific roles
      | name         | description    |
      | BehaveRole1  | Beer Cans      |
      | BehaveRole2  | Silly Walks    |
      | BehaveRole3  | Anvil Dropping |

    When The role information is requested as Org Admin
    Then The role information matches the set of specific roles
      | name         | description    |
      | BehaveRole1  | Beer Cans      |
      | BehaveRole2  | Silly Walks    |
      | BehaveRole3  | Anvil Dropping |


  Scenario: Normal User
    When The role information is requested as a normal user
    Then The response should indicate access is not allowed
