*** Settings ***
Library           ../pywin_tests/SpotifyDesktopApp.py
Resource          elements.robot
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

Wait for mute button to be visible
    wait_for_mute_button

Scroll The Mouse
    volume_scroll    ${volume_amount}    ${volume_direction}

Wait for friends pane to apear
    wait_for_friends_pane_to_be_visible

Click on playlist
    [Arguments]    ${target_playlist}
    click_on_pl    ${target_playlist}

Read Songs from the playlist
    ${songs_for_validation}    read_songs
    set global variable    ${songs_for_validation}
    Log    ${songs_for_validation}    WARN

Validate songs
    validate_song_list    ${songs_for_validation}

Click on homepage
    click_homepage

Connect to spotify Desktop App
    connect_to_spotify

Drag and drop song
    [Arguments]    ${source_playlist}    ${target_playlist}    ${artist_name}    ${song_name}
    move_song_between_playlistsv2    ${source_playlist}    ${target_playlist}    ${artist_name}    ${song_name}

Validate drag and drop functionality
    [Arguments]    ${target_playlist}    ${artist_name}    ${song_name}
    validate_drag_and_drop    ${target_playlist}    ${artist_name}    ${song_name}

Wait for filter field to be present
    wait_for_filter_field

Right click on song in the playlist
    [Arguments]    ${song_name}
    right_click_on_song_in_pl    ${song_name}

Wait for the context menu to remove song
    wait_for_context_menu_remove_song

Click on remove song
    click_remove_song

Validate if song was removed
    [Arguments]    ${song_name}
    validate_remove_song    ${song_name}
