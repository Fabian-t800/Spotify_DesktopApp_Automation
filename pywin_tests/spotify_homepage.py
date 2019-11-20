# from pywinauto.application import Application
from pywinauto import application
from pywinauto.timings import wait_until as pywait

from robot.api import logger
import time

import pywinauto


class SpotifyDesktopApp:

    def __init__(self):
        self.app = None
        self.window_handle = None

    def connect(self):
        # singleton
        try:
            self.app = application.Application(backend='uia', allow_magic_lookup=True).start("Spotify")
        except RuntimeError:
            print("Error")
            logger.console("Application has already started. Proceeding to connect to application.")
        finally:
            self.app.connect(path="Spotify")

        time.sleep(3)
        self.window_handle = self.app.top_window()
        self.window_handle.maximize()

    def search_for_something(self, search_for):
        self.connect()
        # TODO: Needs to add pywinauto wait, otherwise it just fails.
        time.sleep(3)
        # self.window_handle.wait(wait_for="visible enabled ready")
        self.window_handle.wait(wait_for="exists", retry_interval=5)
        # TODO: Needs to add pywinauto wait, otherwise it just fails.
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
            ui_elements_present.append("Song length: " + self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[7].window_text())
            # Time Elapsed timer
            ui_elements_present.append("Time Elapsed timer: " + self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[6].window_text())
            # Repeat Button
            ui_elements_present.append("Repeat button: " + self.window_handle.child_window(auto_id='player-button-repeat').window_text())
            # Next Button
            ui_elements_present.append("Next button: " + self.window_handle.child_window(auto_id='player-button-next').window_text())
            # Play Button
            ui_elements_present.append("Play button: " + self.window_handle.child_window(auto_id='player-button-play').window_text())
            # Previous Button
            ui_elements_present.append("Previous button: " + self.window_handle.child_window(auto_id='player-button-previous').window_text())
            # Shuffle Button
            ui_elements_present.append("Shuffle button: " + self.window_handle.child_window(auto_id='player-button-shuffle').window_text())
            # Currently playing
            ui_elements_present.append("Currently playing title:" + self.window_handle.child_window(auto_id='now-playing-image-large').window_text())
        except IndexError as err:
            logger.console("An element was out of range! The element did not have enough time to load. Error <" + str(err) + "> was thrown.")
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
        selected_pane = self.window_handle.child_window(control_type="Table", found_index=0).children(control_type="Custom")
        songs_list = [child.window_text()
                      for song in self.window_handle.child_window(control_type="Table", found_index=0).children(control_type="Custom")
                      for index, child in enumerate(song.children())
                      if index in [2, 3, 8]]
        # for song in selected_pane:
        #     songs_in_pl.append(song.window_text())
        return songs_list


# SpotifyDesktopApp().search_for_something("Devil")
# print(SpotifyDesktopApp().ui_test_bottom_console())
# print(SpotifyDesktopApp().ui_test_bottom_console())
print(SpotifyDesktopApp().read_songs_from_album())
# print(SpotifyDesktopApp().ui_test_bottom_console())

# Below: Important, Try to use to get to a unique handle

