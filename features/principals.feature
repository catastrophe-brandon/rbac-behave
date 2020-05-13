Feature: Obtain details about principals known to the service

  Scenario: Get the set of principals as an org admin
    Given the RBAC service is running
    And the current user is an org administrator
    When a request is made to obtain principal information
    Then the RBAC service returns the set of known principals


  Scenario: Get the set of principals as a non-org-admin
    Given the RBAC service is running
    And the current user is a non-administrator
    When a request is made to obtain principal information
    Then the RBAC service indicates this operation is prohibited
