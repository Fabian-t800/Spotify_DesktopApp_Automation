*** Settings ***
Library           ../pywin_tests/SpotifyDesktopApp.py
Library           ../pywin_tests/HelperClassSpotifyDesktopApp.py

*** Keywords ***
Click The Search Button
    click_search_button

Wait for middle pane to load
    wait_for_main_middle_pane_to_appear

Clear the search field
    clear_search_field

Enter search kw into search field
    search_for    ${search_kw}

Search Results
    search_res
