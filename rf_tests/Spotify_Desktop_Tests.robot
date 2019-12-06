*** Settings ***
Suite Setup
Suite Teardown
Test Teardown     run keyword if test failed    take screenshot    ${TEST_NAME}
Resource          helper_kw.robot
Resource          elements.robot
Library           Screenshot

*** Test Cases ***
Search feature functionality
    [Tags]    Regression
    Click homepage button
    Search for an item    ${search_term}

Mouse scroll volume functionality
    Change Volume

Read songs from a playlist
    Read songs from a specified playlist

Move song from playlist to playlist
    Click homepage button
    Move song from one playlist to another

Bottom console UI test
    Check to see if all bottom console UI elements are present

Remove song via context menu
    Click homepage button
    Remove a song from a playlist

*** Keywords ***
