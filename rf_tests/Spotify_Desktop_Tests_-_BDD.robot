*** Settings ***
Suite Setup
Resource          elements.robot
Resource          helper_kw2.robot
Library           ../pywin_tests/HelperClassSpotifyDesktopApp.py

*** Test Cases ***
Search Feature Test
    Given Click on homepage
    When Click The Search Button
    And Clear the search field
    When Wait for middle pane to load
    When Enter search kw into search field
    Then Search Results

Mouse Volume Scroll Test
    Given Wait for mute button to be visible
    When Scroll The Mouse

Songs present in playlist Test
    Given Click on homepage
    And Wait for friends pane to apear
    When Click on playlist    ${playlist_nr_read_songs}
    And Wait for middle pane to load
    When Read Songs from the playlist
    Then Validate songs

Move Songs Between Playlists Test
    Given Click on homepage
    And Wait for middle pane to load
    When Drag and drop song    ${source_playlist}    ${target_playlist}    ${name_of_artist_of_song_to_be_moved}    ${song_name_to_be_removed}
    Then Validate drag and drop functionality    ${target_playlist}    ${name_of_artist_of_song_to_be_moved}    ${song_name_to_be_removed}

Remove song from playlist test
    Given Click Homepage
    When Click on playlist    ${playlist_nr_remove_song}
    When Wait for filter field to be present
    Right click on song in the playlist    ${song_name_to_be_removed}
    When Wait for the context menu to remove song
    When Click on remove song
    Then Validate if song was removed    ${song_name_to_be_removed}
