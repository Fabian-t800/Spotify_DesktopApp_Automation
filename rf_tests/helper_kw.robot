*** Settings ***
Library           ../pywin_tests/SpotifyDesktopApp.py

*** Keywords ***
Search for an item
    [Arguments]    ${search_term}
    search_for_something    ${search_term}

Close Spotify desktop app
    close_application

Change volume
    check_volume_mouse_scroll    ${volume_amount}    ${volume_direction}

Read songs from a specified playlist
    read_songs_from_playlist    ${playlist_nr_read_songs}

Move song from one playlist to another
    move_song_between_playlists    ${source_playlist}    ${target_playlist}    ${name_of_artist_of_song_to_be_moved}    ${name_of_song_to_be_moved}

Click homepage button
    click_homepage

Check to see if all bottom console UI elements are present
    ui_test_bottom_console

Remove a song from a playlist
    remove_song_from_playlist_context_menu    ${playlist_nr_remove_song}    ${song_name_to_be_removed}

Connect to the Spotify Desktop App
    connect
