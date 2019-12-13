*** Settings ***
Library           ../pywin_tests/SpotifyDesktopApp.py
Library           ../pywin_tests/HelperClassSpotifyDesktopApp.py

*** Keywords ***
Search for an item
    [Arguments]    ${search_term}
    search_for_something    ${search_term}

Close Spotify desktop app
    close_application

Change volume
    volume_mouse_scroll    ${volume_amount}    ${volume_direction}

Read songs from a specified playlist
    read_songs_from_playlist    ${playlist_nr_read_songs}

Move song from one playlist to another
    move_song_between_playlists    ${source_playlist}    ${target_playlist}    ${name_of_artist_of_song_to_be_moved}    ${name_of_song_to_be_moved}

Click homepage button
    click_homepage

Check to see if all bottom console UI elements are present
    dt_player_ui_test

Remove a song from a playlist
    remove_song_from_playlist_context_menu    ${playlist_nr_remove_song}    ${song_name_to_be_removed}

Connect to the Spotify Desktop App
    connect

Open Menu
    click_menu_item    ${menu_item_name}

Check toggle functionality
    check_toggles_functionality     ${menu_item_name}    ${toggle_button_name}

Run song functionality test
    check_play_song_functionality
