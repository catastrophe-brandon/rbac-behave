Feature: Obtain RBAC service status

  Scenario: Basic Status Check when service is up
    Given the RBAC service is running
    When A request is made to check the status
    Then The service indicates it is operational
