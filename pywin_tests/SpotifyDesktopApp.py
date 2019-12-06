from pywinauto import application
from pywinauto.timings import wait_until as pywait
from robot.api import logger as robologger
import pywinauto
import psutil
import timeit


# TODO: Test teardown -> la orice fail sa faca screenshot (ROBOT)
# TODO: Future: TimeIt => pentru benchamarking


class SpotifyDesktopApp:

    def __init__(self):
        self.app = None
        self.window_handle = None
        self.connect()

    def connect(self):
        """
        :return: Connects to or starts an instance of the Spotify desktop app.
        """
        try:
            pywinauto.application.Application(backend='uia').connect(path="Spotify.exe").is_process_running()
        except pywinauto.application.ProcessNotFoundError:
            self.app = application.Application(backend='uia', allow_magic_lookup=True).start("Spotify")
            self.app.connect(path="Spotify")
            self.window_handle = self.app.top_window()
            self.window_handle.maximize()
        except pywinauto.uia_defines.NoPatternInterfaceError as err:
            robologger.console(f"The <{err}> error has occurred trying to connect.")
            self.connect()
        else:
            spotify_pids = []
            for proc in psutil.process_iter():
                if proc.name() == "Spotify.exe":
                    spotify_pids.append(proc.pid)
            for spotify_pid in spotify_pids:
                try:
                    self.app = pywinauto.application.Application(backend='uia').connect(process=spotify_pid)
                    try:
                        self.app.windows()[0].maximize()
                    except IndexError:
                        continue
                    self.window_handle = self.app.top_window()
                except RuntimeError as err:
                    robologger.console(f'Error: <{err}> was yielded for PID: {spotify_pid}')
                    continue
        try:
            self.app.top_window().wait('visible', timeout=20, retry_interval=1)
        except RuntimeError:
            robologger.console("Application is already running. Window handle ready.")

    def search_for_something(self, search_for):
        """
        :param search_for: Search term that is will be entered into the search bar.
        :return: A tuple with the first three fields.
        """
        # self.connect()
        # self.window_handle.child_window(auto_id="view-content").wait("visible", timeout=20)
        self.window_handle.child_window(title="Search Spotify").click()
        self.window_handle.child_window(auto_id="view-content").wait("visible", timeout=20)
        self.window_handle.child_window(auto_id="header").children()[2].click_input(double=True)
        self.window_handle.child_window(auto_id="header").children()[2].type_keys("{VK_BACK}")
        self.window_handle.child_window(auto_id="header").children()[2].type_keys(search_for)
        robologger.console(f"Search term < {search_for} > has been entered.")
        self.window_handle.child_window(auto_id="view-content").wait("visible", timeout=5)
        second_field = self.window_handle.child_window(auto_id="view-content").children()[1].children()[0].children()[1].window_text()
        first_field = self.window_handle.child_window(auto_id="view-content").children()[1].children()[0].children()[0].window_text()
        third_field = self.window_handle.child_window(auto_id="view-content").children()[1].children()[0].children()[2].window_text()
        robologger.console(f" First field contains: {first_field} \n Second field: {second_field}. \n Third field: {third_field}.")
        return first_field, second_field, third_field

    def ui_test_bottom_console(self):
        """
        :return: Returns a list of ui elements that were successfully found.
        """
        # self.connect()
        ui_elements_present = []
        self.window_handle.child_window(auto_id='player-button-repeat').wait("visible", timeout=7)
        self.window_handle.child_window(auto_id='view-player-footer').wait('visible', timeout=7)
        try:
            # Song Length
            ui_elements_present.append(
                "Song length: " + self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[
                    7].window_text())
            robologger.console("Song length found.")
            # Time Elapsed timer
            ui_elements_present.append("Time Elapsed timer: " +
                                       self.window_handle.children()[2].children()[0].children()[8].children()[
                                           1].children()[6].window_text())
            robologger.console("Time elapsed timer found.")
            # Repeat Button
            ui_elements_present.append(
                "Repeat button: " + self.window_handle.child_window(auto_id='player-button-repeat').window_text())
            robologger.console("Repeat button found.")
            # Next Button
            ui_elements_present.append(
                "Next button: " + self.window_handle.child_window(auto_id='player-button-next').window_text())
            robologger.console("Next button found.")
            # Play Button
            ui_elements_present.append(
                "Play button: " + self.window_handle.child_window(auto_id='player-button-play').window_text())
            robologger.console("Play button found.")
            # Previous Button
            ui_elements_present.append(
                "Previous button: " + self.window_handle.child_window(auto_id='player-button-previous').window_text())
            robologger.console("Previous button found.")
            # Shuffle Button
            ui_elements_present.append(
                "Shuffle button: " + self.window_handle.child_window(auto_id='player-button-shuffle').window_text())
            robologger.console("Shuffle button found.")
            # Currently playing
            ui_elements_present.append("Currently playing title:" + self.window_handle.child_window(
                auto_id='now-playing-image-large').window_text())
            robologger.console("Currently playing button found.")
        except IndexError as err:
            robologger.warn("An element was out of range! The element did not have enough time to load. Error <" + str(
                err) + "> was thrown.")
            raise IndexError("List index out of range. Not all elements were found.")
        finally:
            return ui_elements_present

    def read_songs_from_playlist(self, playlist):
        """
        :param playlist: Name of the playlist that will have it's songs read
        :return: List of songs of the songs from the playlist.
        """
        self.window_handle.child_window(auto_id='iframe-buddy-list').wait('visible', timeout=10)
        self.find_playlist(playlist=playlist).click_input()
        self.window_handle.child_window(control_type="Table", found_index=0).wait("visible")
        # indexes below:
        # 2: Song name
        # 3: Artist
        # 8: Song length
        songs_list = [child.window_text()
                      for song in self.window_handle.child_window(control_type="Table", found_index=0).children(
                control_type="Custom")
                      for index, child in enumerate(song.children())
                      if index in [2, 3, 8]]
        robologger.console(f"All songs in the list are: {songs_list} \n")
        return songs_list

    def move_song_between_playlists(self, source_playlist, target_playlist, artist_name, song_name):
        """
        :param: source_playlist: The playlist from which you want to drag the song. Order number in the playlist.
        :param: target_playlist: The playlist into which you want to drag the song. Order number in the playlist.
        :param: song_name: Name of the song you want to take from the source playlist. Use entire and correct name.
        :param: artist: Name of the artist that performs the song entered in song_name
        :return: If the song is successfully moved between playlists, returns true.
        """
        self.click_homepage()
        self.window_handle.child_window(auto_id="view-content").wait("ready", timeout=3)
        t_playlist = self.find_playlist(target_playlist)
        robologger.console("Target playlist found and selected.")
        s_playlist = self.find_playlist(source_playlist)
        robologger.console("Source playlist found and selected.")
        s_playlist.click_input()
        robologger.console("Source playlist clicked.")
        self.window_handle.child_window(title="Filter", control_type="Edit").wait("ready", timeout=4)
        robologger.console("Playlist pane ready.")
        song = self.window_handle.child_window(auto_id="view-content", control_type="Group").child_window(title=song_name, found_index=0)
        artist = self.window_handle.child_window(auto_id="view-content", control_type="Group").child_window(title=artist_name, found_index=0)
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
        self.click_homepage()
        self.find_playlist(playlist=playlist).click_input()
        robologger.console("Playlist found and clicked.")
        self.window_handle.child_window(title="Filter", control_type="Edit").wait("ready", timeout=7)
        robologger.console("Playlist items found.")
        song = self.window_handle.child_window(auto_id="view-content", control_type="Group").child_window(title=song_name, found_index=0)
        song.click_input(button='right')
        self.window_handle.child_window(title="Remove from this Playlist").wait("ready", timeout=10)
        remove_button = self.window_handle.child_window(title="Remove from this Playlist")
        remove_button.click_input()
        return "Action was completed successfully!"

    def check_volume_mouse_scroll(self, nr_of_increments, direction=1):
        """
        :param nr_of_increments: 1 increment means 10% change in volume
        :param direction: 1: Increase in volume, -1: Decrease in volume
        :return: Returns nothing.
        """
        self.window_handle.child_window(title="Mute").wait("visible", timeout=7)
        for i in range(0, int(nr_of_increments)):
            self.window_handle.child_window(title="Mute").move_mouse_input(coords=(50, 20), absolute=False).wheel_mouse_input(coords=(50, 20), wheel_dist=int(direction))

    def toggles(self, toggle_button_description):
        """
        :return: A tuple: Current state: the state before any action was executed on the toggle button. Final state: the state of the toggle button after the action.
        """
        # Click menu
        self.window_handle.wait('visible', timeout=5)
        settings_menu_expand_button = self.settings_menu()
        try:
            settings_menu_expand_button.wait('visible', timeout=5)
            settings_menu_expand_button.click_input()
            # Select settings menu item
            settings_menu_item = self.window_handle.child_window(title='Settings', control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        except pywinauto.timings.TimeoutError as err:
            robologger.console(f'Error <{err}> has occurred. Proceeding to click.')
            settings_menu_expand_button.click_input()
            settings_menu_item = self.window_handle.child_window(title='Settings', control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        finally:
            settings_menu_item.draw_outline()
            settings_menu_item.click_input()
        # explicit_content_toggle = self.window_handle.child_window(control_type='CheckBox', title='Allow playback of explicit-rated content.')
        explicit_content_toggle = self.toggle_button(toggle_button_description)
        explicit_content_toggle.wait('visible', timeout=5)
        explicit_content_toggle.draw_outline()
        current_state = explicit_content_toggle.get_toggle_state()
        explicit_content_toggle.toggle()
        final_state = explicit_content_toggle.get_toggle_state()
        return current_state, final_state
        # current_state = explicit_content_toggle.get_toggle_state()
        # robologger.console(f'Initial state is {current_state}')
        # explicit_content_toggle.toggle()
        # final_state = explicit_content_toggle.get_toggle_state()
        # robologger.console(f'Final state is {final_state}')

    def close_application(self):
        self.window_handle.close()

    def click_homepage(self):
        self.window_handle.child_window(title="Home").click_input()

    def find_playlist(self, playlist):
        try:
            pl = self.window_handle.child_window(auto_id='view-navigation-bar').child_window(title=playlist, found_index=0)
        except pywinauto.findwindows.ElementNotFoundError as err:
            robologger.console(f"The <{err}> has occured. Element was not found.")
        else:
            return pl

    def play_button(self):
        """
        :returns: Play button object
        """
        self.window_handle.child_window(auto_id='player-button-play').wait('visible', 10)
        return self.window_handle.child_window(auto_id='player-button-play')

    def mute_button(self):
        """
        :return: Mute button object
        """
        return self.window_handle.child_window(title="Mute")

    def settings_menu(self):
        """
        :return: Settings menu object.
        """
        return self.window_handle.child_window(auto_id='profile-menu-toggle')

    def toggle_button(self, toggle_name):
        """
        :param toggle_name: Name of the toggle option
        :return: Toggle button for the
        """
        try:
            return self.window_handle.child_window(control_type='CheckBox', title=toggle_name)
        except pywinauto.ElementNotFoundError:
            robologger.console("Element was not found.")

    def check_toggle(self, toggle_result):
        """
        :param toggle_result: uses the SpotifyDesktopApp().toggles() as input
        :return: Returns True if the toggle has worked, else returns False
        """
        if toggle_result == (0, 0) or toggle_result == (1, 1):
            robologger.console('An error has occurred. Toggling has not been achieved.')
            return False
        else:
            robologger.console("The toggle option has worked.")
            return True

    def player_ui_control(self, ui_elements):
        if len(ui_elements) is 8:
            robologger.console("All the elements are present")
            print(ui_elements)
            return True
        else:
            robologger.console("There are less elements than expected. Test has failed.")


if __name__ == '__main__':

    result = SpotifyDesktopApp().toggles("Allow playback of explicit-rated content.")
    SpotifyDesktopApp().check_toggle(result)
    # SpotifyDesktopApp().toggle_button("Make my new playlists public").click_input()
    # print(SpotifyDesktopApp().read_songs_from_playlist('Super_jazz'))
    # print(SpotifyDesktopApp().ui_test_bottom_console())
    # print(SpotifyDesktopApp().move_song_between_playlists
    #     (
    #     source_playlist='extra_heavy_metal',
    #     target_playlist='Super_jazz',
    #     artist_name='Soilwork',
    #     song_name='Stabbing the Drama'
    #     ))

    # print(SpotifyDesktopApp().remove_song_from_playlist_context_menu("extra_heavy_metal", "Strangler"))
    # SpotifyDesktopApp().toggles()
    # SpotifyDesktopApp().find_playlist('extra_heavy_metal').click_input()
    # print(SpotifyDesktopApp().window_handle
    pass
