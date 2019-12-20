import pywin_tests.SpotifyDesktopApp as SDA
from robot.api import logger as robologger
from dateutil.parser import parse
import time
import pywinauto


class HelperClassSpotifyDesktopApp:

    def __init__(self):
        self.sda = SDA.SpotifyDesktopApp()

    def search_for_something(self, search_for):
        """
        :param search_for: Search term that is will be entered into the search bar.
        :return: A tuple with the first three fields.
        """
        self.sda.homepage_button().click_input()
        self.sda.search_field_icon().click()
        self.sda.main_middle_pane().wait("visible", timeout=20)
        self.sda.search_field().click_input(double=True)
        self.sda.search_field().type_keys("{VK_BACK}")
        self.sda.search_field().type_keys(search_for)
        robologger.console(f"Search term < {search_for} > has been entered.")
        self.sda.main_middle_pane().wait("visible", timeout=5)
        first_field = self.sda.search_result_field_one().window_text()
        second_field = self.sda.search_result_field_two().window_text()
        third_field = self.sda.search_result_field_three().window_text()
        robologger.console(f" First field contains: {first_field} \n "
                           f"Second field: {second_field}. \n "
                           f"Third field: {third_field}.")
        return first_field, second_field, third_field

    def read_songs_from_playlist(self, playlist):
        """
        :param playlist: Name of the playlist that will have it's songs read
        :return: List of songs of the songs from the playlist.
        """
        # TODO: Need to read all songs from the playlist
        # Needs scroll functionality implemented
        # Until it gets to the recommended songs menu item
        self.sda.friends_pane().wait('visible', timeout=10)
        self.sda.find_playlist(playlist=playlist).click_input()
        self.sda.table_of_songs().wait('visible', timeout=10)
        # indexes below:
        # 2: Song name
        # 3: Artist
        # 8: Song length
        songs_list = [child.window_text()
                      for song in self.sda.window_handle.child_window(control_type="Table", found_index=0).children(
                control_type="Custom")
                      for index, child in enumerate(song.children())
                      if index in [2, 3, 8]]
        robologger.console(f"All songs in the list are: {songs_list} \n")
        return songs_list

    def connect_to(self):
        self.sda = SDA.SpotifyDesktopApp()
        self.handle = self.sda.connect()
        self.sda.set_handle(self.handle)

    def move_song_between_playlists(self, source_playlist, target_playlist, artist_name, song_name):
        """
        :param: source_playlist: The playlist from which you want to drag the song. Order number in the playlist.
        :param: target_playlist: The playlist into which you want to drag the song. Order number in the playlist.
        :param: song_name: Name of the song you want to take from the source playlist. Use entire and correct name.
        :param: artist: Name of the artist that performs the song entered in song_name
        :return: If the song is successfully moved between playlists, returns true.
        """
        self.sda.homepage_button().click_input()
        self.sda.main_middle_pane().wait("visible", timeout=3)
        t_playlist = self.sda.find_playlist(target_playlist)
        robologger.console("Target playlist found and selected.")
        s_playlist = self.sda.find_playlist(source_playlist)
        robologger.console("Source playlist found and selected.")
        s_playlist.click_input()
        robologger.console("Source playlist clicked.")
        self.sda.filter_field().wait("visible", timeout=4)
        robologger.console("Playlist pane ready.")
        song = self.sda.song_in_playlist(song_name)
        artist = self.sda.artist_in_playlist(artist_name)
        if song.window_text() == song_name and artist.window_text() == artist_name:
            song.draw_outline()
            t_playlist.draw_outline()
            song.drag_mouse_input(dst=t_playlist.children()[0])
            robologger.console(f' The drag and drop operation was successful. \n {song_name} was dragged from {source_playlist} playlist to the playlist named {target_playlist}.')
            return True
        else:
            robologger.console("Song or artist not in the source playlist!")

    def remove_song_from_playlist_context_menu(self, playlist, song_name):
        """
        :param song_name: Song name that you want to delete.
        :param playlist: The playlist from which you want to delete the song. Integer value.
        :return: Returns nothing.
        """
        self.sda.homepage_button().click_input()
        self.sda.find_playlist(playlist=playlist).click_input()
        robologger.console("Playlist found and clicked.")
        self.sda.filter_field().wait("ready", timeout=7)
        robologger.console("Playlist items found.")
        self.sda.song_in_playlist(song_name).click_input(button='right')
        self.sda.rc_context_menu("Remove from this Playlist").wait('visible', timeout=7)
        self.sda.rc_context_menu("Remove from this Playlist").click_input()
        return "Action was completed successfully!"

    def volume_mouse_scroll(self, nr_of_increments, direction=1):
        """
        :param nr_of_increments: 1 increment means 10% change in volume
        :param direction: 1: Increase in volume, -1: Decrease in volume
        :return: Returns nothing.
        """
        self.sda.mute_button().wait("visible", timeout=7)
        for i in range(0, int(nr_of_increments)):
            self.sda.mute_button().move_mouse_input(coords=(50, 20), absolute=False).wheel_mouse_input(coords=(50, 20), wheel_dist=int(direction))

    def toggles(self, toggle_button_description):
        """
        :param toggle_button_description: The name of the toggle button
        :return:
        """
        toggle_button = self.sda.toggle_button(toggle_button_description)
        toggle_button.wait('visible', timeout=5)
        toggle_button.draw_outline()
        toggle_button.toggle()

    def click_menu_item(self, menu_item_name):
        """
        :param menu_item_name:  name of the menu item
        :return:  Clicks on the menu item
        """
        self.sda.window_handle.wait('visible', timeout=5)
        settings_menu_expand_button = self.sda.settings_menu()
        try:
            settings_menu_expand_button.wait('visible', timeout=5)
            settings_menu_expand_button.click_input()
            # Select settings menu item
            settings_menu_item = self.sda.window_handle.child_window(title=menu_item_name, control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        except pywinauto.timings.TimeoutError as err:
            robologger.console(f'Error <{err}> has occurred. Proceeding to click.')
            settings_menu_expand_button.click_input()
            settings_menu_item = self.sda.window_handle.child_window(title='Settings', control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        finally:
            settings_menu_item.draw_outline()
            settings_menu_item.click_input()

    def check_toggles_functionality(self, menu_item_name, toggle_button_name):
        """
        :param menu_item_name: Name of the menu item that should be clicked
        :param toggle_button_name: Name (description of the toggle item
        :return:
        """
        self.click_menu_item(menu_item_name)
        current_state = self.sda.toggle_button(toggle_button_name).get_toggle_state()
        self.toggles(toggle_button_name)
        final_state = self.sda.toggle_button(toggle_button_name).get_toggle_state()
        if current_state != final_state:
            # robologger.console(f" Current state was {current_state} \n Final state is {final_state}.")
            robologger.console("Toggle function works.")
            return True
        else:
            robologger.warn("The toggle function did not function!")
            return False

    def check_play_song_functionality(self):
        """
        :return: Returns True if the song is played correctly
        """
        initial_time = parse(self.sda.time_elapsed().window_text()).time()
        self.play_song(2)
        if initial_time < parse(self.sda.time_elapsed().window_text()).time():
            robologger.console("The song has successfully been played.")
            return True
        else:
            robologger.error("The song has not been played.")
            return False

    def dt_player_ui_test(self):
        """
        :return:  If all UI elements are present, returns True
        """
        error_flag = False
        try:
            assert (self.sda.song_length()), 'Song length not found.'
        except AssertionError:
            robologger.error("The song length element was not found")
            error_flag = True
        try:
            assert (self.sda.shuffle_button()), 'Shuffle button not found.'
        except AssertionError:
            robologger.error("The shuffle button element was not found")
            error_flag = True
        try:
            assert (self.sda.mute_button()), 'Mute button not found.'
        except AssertionError:
            robologger.error("The mute button element was not found")
            error_flag = True
        try:
            assert (self.sda.play_button()), 'Play button not found.'
        except AssertionError:
            robologger.error("The play button element was not found")
            error_flag = True
        try:
            assert (self.sda.previous_button()), 'Previous song button not found.'
        except AssertionError:
            robologger.error("The Previous song button element was not found")
            error_flag = True
        try:
            assert (self.sda.next_button()), 'Next song button not found.'
        except AssertionError:
            robologger.error("The Next song button element was not found")
            error_flag = True
        try:
            assert (self.sda.currently_playing()), 'Currently playing panel is not found.'
        except AssertionError:
            robologger.error("The Currently playing button element was not found")
            error_flag = True
        try:
            assert (self.sda.repeat_button()), 'Repeat button is not found.'
        except AssertionError:
            robologger.error("The repeat button element was not found")
            error_flag = True
        try:
            assert (self.sda.time_elapsed()), 'Time elapsed not found.'
        except AssertionError:
            robologger.error("The time elapsed element was not found")
            error_flag = True

        if error_flag is False:
            robologger.console("All ui elements are present.")
            return True
        else:
            return False

    def play_song(self, time_to_play):
        """
        :param time_to_play: how long the song should be played for
        :return:
        """
        self.sda.play_button().wait('visible', timeout=5)
        self.sda.play_button().click_input()
        time.sleep(time_to_play)
        self.sda.play_button().click_input()

    def click_homepage(self):
        """
        :return: Clicks the homepage object.
        """
        self.sda.homepage_button().click_input()

    def close_application(self):
        """
        :return: Closes the Spotify Desktop App
        """
        self.sda.window_handle.close()

    def click_search_button(self):
        self.sda.search_field_icon().click()

    def wait_for_main_middle_pane_to_appear(self):
        self.sda.main_middle_pane().wait("visible", timeout=20)

    def clear_search_field(self):
        self.sda.search_field().click_input(double=True)
        self.sda.search_field().type_keys("{VK_BACK}")

    def search_for(self, search_term):
        self.sda.search_field().type_keys(search_term)

    def search_res(self):
        if (self.sda.search_result_field_one().window_text() and self.sda.search_result_field_two().window_text() and self.sda.search_result_field_three().window_text()) is not None:
            return True
        else:
            raise AssertionError
        # return self.sda.search_result_field_one().window_text(), self.sda.search_result_field_two().window_text(), self.sda.search_result_field_three().window_text()

    def wait_for_mute_button(self):
        self.sda.mute_button().wait("visible", timeout=7)

    def volume_scroll(self, nr_of_increments, direction=1):
        """
        :param nr_of_increments: 1 increment means 10% change in volume
        :param direction: 1: Increase in volume, -1: Decrease in volume
        :return: Returns nothing.
        """
        for i in range(0, int(nr_of_increments)):
            self.sda.mute_button().move_mouse_input(coords=(50, 20), absolute=False).wheel_mouse_input(coords=(50, 20),
                                                                                                       wheel_dist=int(
                                                                                                           direction))

    def wait_for_friends_pane_to_be_visible(self):
        self.sda.friends_pane().wait('visible', timeout=10)

    def click_on_pl(self, playlist_name):
        self.sda.find_playlist(playlist=playlist_name).click_input()

    def read_songs(self):
        song_list = [child.window_text()
                      for song in self.sda.window_handle.child_window(control_type="Table", found_index=0).children(control_type="Custom")
                      for index, child in enumerate(song.children())
                      if index in [2, 3, 8]]
        robologger.console(f"All songs in the list are: {song_list} \n")
        return song_list

    def validate_song_list(self, song_list):
        if len(song_list) != 0:
            return True
        else:
            raise AssertionError("There are no songs in your playlist!")

    def move_song_between_playlistsv2(self, source_playlist, target_playlist, artist_name, song_name):
        """
        :param: source_playlist: The playlist from which you want to drag the song. Order number in the playlist.
        :param: target_playlist: The playlist into which you want to drag the song. Order number in the playlist.
        :param: song_name: Name of the song you want to take from the source playlist. Use entire and correct name.
        :param: artist: Name of the artist that performs the song entered in song_name
        :return: If the song is successfully moved between playlists, returns true.
        """
        t_playlist = self.sda.find_playlist(target_playlist)
        s_playlist = self.sda.find_playlist(source_playlist)
        s_playlist.click_input()
        robologger.console("Source playlist clicked.")
        self.sda.filter_field().wait("visible", timeout=4)
        robologger.console("Playlist pane ready.")
        song = self.sda.song_in_playlist(song_name)
        artist = self.sda.artist_in_playlist(artist_name)
        if song.window_text() == song_name and artist.window_text() == artist_name:
            song.draw_outline()
            t_playlist.draw_outline()
            song.drag_mouse_input(dst=t_playlist.children()[0])
        else:
            robologger.console("Song or artist not in the source playlist!")

    def validate_drag_and_drop(self, target_playlist, artist_name, song_name):
        self.sda.find_playlist(target_playlist).click_input()
        self.sda.filter_field().wait("visible", timeout=4)
        song = self.sda.song_in_playlist(song_name)
        artist = self.sda.artist_in_playlist(artist_name)
        if song.window_text() == song_name and artist.window_text() == artist_name:
            robologger.console("The drag and drop functionality has worked.")
        else:
            robologger.console("The drag and drop functionality failed.")
            raise AssertionError(f"Expection that the {target_playlist} should contain the {song_name}, by the artist {artist_name}. \n It was not found")

    def wait_for_filter_field(self):
        self.sda.filter_field().wait("ready", timeout=7)

    def right_click_on_song_in_pl(self, song_name):
        self.sda.song_in_playlist(song_name).click_input(button='right')

    def wait_for_context_menu_remove_song(self):
        self.sda.rc_context_menu("Remove from this Playlist").wait('visible', timeout=7)

    def click_remove_song(self):
        self.sda.rc_context_menu("Remove from this Playlist").click_input()

    def validate_remove_song(self, song_name):
        song = self.sda.song_in_playlist(song_name)
        try:
            song.window_text() == song_name
        except pywinauto.ElementNotFoundError:
            robologger.console("The song was successfully removed from the playlist.")
        else:
            raise AssertionError(f"Expected outcome: {song_name} was removed from the playlist. Instead {song_name} is still present.")

    def wait_for_play_button(self):
        self.sda.play_button().wait('visible', timeout=5)

    def click_play_button(self):
        self.sda.play_button().click_input()

    def read_time_before(self):
        return parse(self.sda.time_elapsed().window_text()).time()

    def read_time_after(self):
        return parse(self.sda.time_elapsed().window_text()).time()

    def wait_time(self, time_to_wait):
        time.sleep(int(time_to_wait))

    def validate_play_song(self, intial_time, final_time):
        if intial_time < final_time:
            robologger.console("The song was successfully played.")
        else:
            raise AssertionError(f"The expected result was {intial_time} < {final_time}.")

    def read_initial_toggle_state(self, toggle_button_name):
        return self.sda.toggle_button(toggle_button_name).get_toggle_state()

    def read_final_toggle_state(self, toggle_button_name):
        return self.sda.toggle_button(toggle_button_name).get_toggle_state()

    def validate_toggle_function(self, initial_toggle_state, final_toggle_state):
        if initial_toggle_state != final_toggle_state:
            robologger.console("Toggle functionality works.")
        else:
            raise AssertionError(f" The expected result would be that the initial toggle state should be different to the final toggle state.\n The current situation is that the initial state is {initial_toggle_state} and the final state was {final_toggle_state}.")

    def close_alert_pane(self):
        try:
            self.sda.alert_pane().click_input()
        except pywinauto.ElementNotFoundError:
            pass



# if __name__ == '__main__':
#
#     p = HelperClassSpotifyDesktopApp()
#     p.close_alert_pane()

    # p.click_homepage()
    # p.wait_for_play_button()
    # before = p.read_time_after()
    # p.click_play_button()
    # p.wait_time(2)
    # p.click_play_button()
    # after = p.read_time_after()
    # p.validate_play_song(before, after)
    # p.wait_for_main_middle_pane_to_appear()
    # p.click_on_pl("extra_heavy_metal")
    # results = p.read_songs()
    # print(p.validate_song_list(results))
#     p.click_search_button()
#     p.wait_for_main_middle_pane_to_appear()
#     p.clear_search_field()
#     p.search_for("Strangler")
#     print(p.search_results())
    # Passed tests:
    # p.search_for_something("Strangler")
    # p.check_toggles_functionality("Settings", "Allow playback of explicit-rated content.")
    # p.read_songs_from_playlist("Workout_songs")
    # p.dt_player_ui_test()
    # p.check_play_song_functionality()
    # p.remove_song_from_playlist_context_menu("Super_jazz", "Summer Love")
    # p.move_song_between_playlists(source_playlist="extra_heavy_metal", target_playlist="Super_jazz", artist_name="Soilwork", song_name="Strangler")
    # p.check_toggles_functionality("Settings", "Allow playback of explicit-rated content.")
