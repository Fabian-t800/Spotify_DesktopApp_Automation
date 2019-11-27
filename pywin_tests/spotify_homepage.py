from pywinauto import application
from pywinauto.timings import wait_until as pywait
from robot.api import logger
import time
import pywinauto

# TODO: Change all time.sleep()'s to pywinauto's wait methods
# TODO: Modificare children.children() ===> automation_id cumva
# TODO: Wait visible = > pentru stabilitate in cod (unde se poate)
# TODO: Layer de robot
# TODO: Definire de actiuni de baza
# TODO: Helper Classes
# TODO: Test teardown -> la orice fail sa faca screenshot (ROBOT)
# TODO: Optimizare connect()
# TODO: Future: TimeIt => pentru benchamarking


class SpotifyDesktopApp:

    def __init__(self):
        self.app = None
        self.window_handle = None
        self.connect2()

    def connect(self):
        try:
            self.app = application.Application(backend='uia', allow_magic_lookup=True).start("Spotify")
        except RuntimeError as err:
            print(err)
            logger.console("Application has already started. Proceeding to connect to application.")
        finally:
            self.app.connect(path="Spotify")

        self.window_handle = self.app.top_window()
        self.window_handle.maximize()

    # def connect2(self):
    #     try:
    #         self.app = application.Application

        #
        # if self.app is None:
        #     self.app = application.Application(backend='uia', allow_magic_lookup=True).start("Spotify")
        #     print("If branch.")
        # elif self.app is not None:
        #     self.app = application.Application(backend='uia', allow_magic_lookup=True).connect(path="Spotify.exe")
        #     print("Else branch.")

    def search_for_something(self, search_for):
        """
        :param search_for: Search term that is will be entered into the search bar.
        :return:
        """
        self.connect()
        self.window_handle.child_window(auto_id="view_content").wait("ready", timeout=20)
        self.window_handle.children()[2].children()[0].children()[4].children()[2].children()[0].click()
        self.window_handle.child_window(title="Search Spotify").type_keys(search_for)
        # works until here
        # below is experimental
        # check and see first few elements

    def ui_test_bottom_console(self):
        self.connect()
        ui_elements_present = []
        self.window_handle.child_window(auto_id='player-button-repeat').wait("ready", timeout=5)

        try:
            # Song Length
            ui_elements_present.append(
                "Song length: " + self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[
                    7].window_text())
            # Time Elapsed timer
            ui_elements_present.append("Time Elapsed timer: " +
                                       self.window_handle.children()[2].children()[0].children()[8].children()[
                                           1].children()[6].window_text())
            # Repeat Button
            ui_elements_present.append(
                "Repeat button: " + self.window_handle.child_window(auto_id='player-button-repeat').window_text())
            # Next Button
            ui_elements_present.append(
                "Next button: " + self.window_handle.child_window(auto_id='player-button-next').window_text())
            # Play Button
            ui_elements_present.append(
                "Play button: " + self.window_handle.child_window(auto_id='player-button-play').window_text())
            # Previous Button
            ui_elements_present.append(
                "Previous button: " + self.window_handle.child_window(auto_id='player-button-previous').window_text())
            # Shuffle Button
            ui_elements_present.append(
                "Shuffle button: " + self.window_handle.child_window(auto_id='player-button-shuffle').window_text())
            # Currently playing
            ui_elements_present.append("Currently playing title:" + self.window_handle.child_window(
                auto_id='now-playing-image-large').window_text())
        except IndexError as err:
            logger.console("An element was out of range! The element did not have enough time to load. Error <" + str(
                err) + "> was thrown.")
            logger.info("An element index was out of range error.")
        finally:
            if len(ui_elements_present) == 8:
                return ui_elements_present
            else:
                return "Not all elements were found."
        # TODO: Remove Window_handle.close when adapting to RF
        self.window_handle.close()

    def read_songs_from_album(self):
        self.connect()
        songs_in_pl = []
        time.sleep(4)
        playlist_pane = self.window_handle.children()[2].children()[0].children()[1].children()[2]
        time.sleep(2)
        playlist_pane.children()[1].click_input()
        time.sleep(2)
        # Selected playlist pane
        # selected_pane = self.window_handle.children()[2].children()[0].children()[5].children()[1].children()[0].children()[6].children(control_type="Custom",)
        selected_pane = self.window_handle.child_window(control_type="Table", found_index=0).children(
            control_type="Custom")
        songs_list = [child.window_text()
                      for song in self.window_handle.child_window(control_type="Table", found_index=0).children(
                control_type="Custom")
                      for index, child in enumerate(song.children())
                      if index in [2, 3, 8]]
        # for song in selected_pane:
        #     songs_in_pl.append(song.window_text())
        return songs_list

    def move_song_between_playlists(self, source_playlist, target_playlist, artist, song_name):
        """
        :param source_playlist: The playlist from which you want to drag the song. Order number in the playlist.
        :param target_playlist: The playlist into which you want to drag the song. Order number in the playlist.
        :param song_name: Name of the song you want to take from the source playlist. Use entire and correct name.
        :param artist: Name of the artist that performs the song entered in song_name
        :return:
        """
        # TODO: Try to make it work wihout loops
        self.connect()
        if isinstance(target_playlist, int):
            # Use the index-1 strategy
            self.window_handle.child_window(auto_id="view-content").wait("ready", timeout=3)
            t_playlist = self.window_handle.child_window(title="Your Library and Playlists").children()[2].children()[
                target_playlist - 1]

        if isinstance(source_playlist, int):
            # Use the index - 1 strategy
            s_playlist = \
            self.window_handle.child_window(title="Your Library and Playlists").children()[2].children()[0].children()[
                source_playlist - 1]
            self.window_handle.child_window(auto_id="view-content").wait("ready", timeout=3)
            s_playlist.click_input()
            self.window_handle.child_window(title="Filter", control_type="Edit").wait("ready", timeout=4)
            playlist_pane = self.window_handle.child_window(auto_id="view-content", control_type="Group")
            songs_in_pl = playlist_pane.children()[1].children()[0].children()[6].children(control_type="Custom")
            for i in range(1, len(songs_in_pl)):
                if songs_in_pl[i].children()[3].window_text() == artist and songs_in_pl[i].children()[2].window_text() == song_name:
                    songs_in_pl[i].children()[2].drag_mouse_input(dst=t_playlist)
                    return "Drag from source playlist to target playlist was completed successfully."
        else:
            # use the if playlist.children().children().title == source_playlist
            pass

    def remove_song_from_playlist_context_menu(self, playlist_nr, song_name):
        """
        :param song_name: Song name that you want to delete.
        :param playlist_nr: The playlist from which you want to delete the song. Integer value.
        :return:
        """
        self.connect()
        # self.window_handle.child_window(auto_id="view-content").wait("ready", timeout=7)
        time.sleep(5)
        playlist = self.window_handle.child_window(title="Your Library and Playlists").children()[2].children()[0].children()[playlist_nr - 1]
        playlist.click_input(button="left")
        self.window_handle.child_window(title="Filter", control_type="Edit").wait("ready", timeout=7)
        playlist_pane = self.window_handle.child_window(auto_id="view-content", control_type="Group")
        songs_in_pl = playlist_pane.children()[1].children()[0].children()[6].children(control_type="Custom")
        for i in range(1, len(songs_in_pl)):
            if songs_in_pl[i].children()[2].window_text() == song_name:
                songs_in_pl[i].children()[2].click_input(button="right")
                this_page = self.window_handle.children()[2].children()[0].children()
                time.sleep(3)
                for j in range(0, len(this_page)):
                    if this_page[j].window_text() == "Remove from this Playlist":
                        this_page[j].click_input()
                        break
                break

    def check_volume_mouse_scroll(self, nr_of_increments, direction=1):
        """
        :param nr_of_increments: 1 increment means 10% change in volume
        :param direction: 1: Increase in volume, -1: Decrease in volume
        :return:
        """
        self.connect()
        self.window_handle
        # Below: incrementation is by 10% every time
        for i in range(0, nr_of_increments):
            self.window_handle.child_window(title="Mute").move_mouse_input(coords=(50, 20), absolute=False).wheel_mouse_input(coords=(50, 20), wheel_dist=direction)

    def toggles(self):
        self.connect()
        # Click menu

        # main_menu = self.window_handle.children()[2].children()[0].children()[4].children()[6]
        self.window_handle.wait('visible', timeout=5)
        settings_menu_expand_button = self.window_handle.child_window(auto_id='profile-menu-toggle')
        try:
            settings_menu_expand_button.wait('visible', timeout=5)
            settings_menu_expand_button.click_input()
            # Select settings menu item
            settings_menu_item = self.window_handle.child_window(title='Settings', control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        except pywinauto.timings.TimeoutError:
            print('except')
            settings_menu_expand_button.click_input()
            settings_menu_item = self.window_handle.child_window(title='Settings', control_type='MenuItem')
            settings_menu_item.wait('visible', timeout=5)
        finally:
            settings_menu_item.draw_outline()
            settings_menu_item.click_input()
        # self.window_handle.children()[2].children()[0].children()[4].children()[6].move_mouse_input(coords=(0, 160), absolute=False)
        explicit_content_toggle = self.window_handle.child_window(control_type='CheckBox', title='Allow playback of explicit-rated content.')
        explicit_content_toggle.wait('visible', timeout=5)
        explicit_content_toggle.draw_outline()
        current_state = explicit_content_toggle.get_toggle_state()
        print(f'Initial state is {current_state}')
        explicit_content_toggle.toggle()
        final_state = explicit_content_toggle.get_toggle_state()
        print(f'Final state is {final_state}')

        print("qq")
        pass



# SpotifyDesktopApp().search_for_something("Devil")
# print(SpotifyDesktopApp().read_songs_from_album())
# print(SpotifyDesktopApp().ui_test_bottom_console())
# print(SpotifyDesktopApp().move_song_between_playlists(1, 2, "Soilwork", "Distortion Sleep"))
# print(SpotifyDesktopApp().remove_song_from_playlist_context_menu(1, "Strangler"))
# SpotifyDesktopApp().check_volume_mouse_scroll(3)
# SpotifyDesktopApp().toggles()
# SpotifyDesktopApp().connect2()
app = application.Application.connect("Spotify.exe")
