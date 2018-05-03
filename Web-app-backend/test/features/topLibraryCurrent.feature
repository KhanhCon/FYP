Feature: Get top most popular libraries
  Scenario Outline: Get current usage
    Given Database and graph
    When Query the most popular libraries at currently
    Then <library> has <usage> usage

    Examples: UsagesCurrent
    | library | usage |
    | A       | 0     |
    | B       | 0     |
    | C       | 2     |
    | D       | 0     |
    | E       | 1     |
    | F       | 0     |