# -- FILE: features/example.feature
Feature: Get top most popular libraries at date

#  Scenario: Get top 6 most popular libraries currently
#    Given Database and graph
#    When Query the top 6 most popular libraries currently
#    Then We get 6 results
#    Then C has 2 usage, E has 1 usage, F has 0 usage currently
#
#  Scenario: Get the most popular libraries at 2018-01-01
#    Given Database and graph
#    When Query the most popular libraries at 2018-01-01
#    Then C has 2 usage, E has 0 usage, F has 0 usage at 2018-01-01

  Scenario Outline: Get usage of C
    Given Database and graph
    When Query the most popular libraries at <date>
    Then C has <usageC> usage

    Examples: UsagesC
    | date          | usageC |
    | "2017-05-04"  | 0      |
    | "2017-05-05"  | 1      |
    | "2017-05-06"  | 1      |
    | "2017-10-09"  | 1      |
    | "2017-10-09"  | 1      |
    | "2017-10-10"  | 1      |
    #Boundaries where it has 2 usages
    | "2017-11-29"  | 1      |
    | "2017-12-01"  | 2      |
    | "2017-12-02"  | 2      |
    | "2018-01-15"  | 2      |
    | "2018-03-01"  | 2      |
    | "2018-03-02"  | 2      |
    | "2018-03-03"  | 2      |

  Scenario Outline: Get usage of E
    Given Database and graph
    When Query the most popular libraries at <date>
    Then E has <usageE> usage

    Examples: UsagesE
    | date          | usageE |
    | "2018-01-01"  | 0      |
    | "2018-01-02"  | 1      |
    | "2018-01-03"  | 1      |


#  Scenario: Get the most popular libraries at 2017-05-05
#    Given Database and graph
#    When Query the most popular libraries at "2017-05-05"
#    Then C has 1 usage at 2017-05-05

#  Scenario: Get the most popular libraries at 2017-10-09
#    Given Database and graph
#    When Query the most popular libraries at 2017-10-09
#    Then C has 1 usage at 2017-10-09
#
#  Scenario: Get the most popular libraries at 2017-10-10
#    Given Database and graph
#    When Query the most popular libraries at 2017-10-10
#    Then C has 1 usage at 2017-10-10
#
#  Scenario: Get the most popular libraries at 2017-10-11
#    Given Database and graph
#    When Query the most popular libraries at 2017-10-11
#    Then C has 1 usage at 2017-10-11
