Feature: Obtain details about groups known to the RBAC service

  Scenario: Get the group data as an org admin
    Given the RBAC service is running
    And the current user is an org administrator
    When a request is made to obtain group information
    Then the RBAC service returns the set of known groups


  Scenario: Get the groups data as a non-org-admin
    Given the RBAC service is running
    And the current user is a non-administrator
    When a request is made to obtain group information
    Then the RBAC service returns the set of known groups
