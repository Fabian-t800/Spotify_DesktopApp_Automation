*** Settings ***
Resource          elements.robot
Resource          helper_kw2.robot

*** Test Cases ***
Search Feature Test
    Given Click Homepage
    When Click The Search Button
    And Clear the search field
    When Wait for middle pane to load
    When Enter search kw into search field
    Then Search Results
