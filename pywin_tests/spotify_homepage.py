# from pywinauto.application import Application
from pywinauto import application
from pywinauto.timings import wait_until

from robot.api import logger
import time

import pywinauto


# TODO: These are the elements of the lower console
# window_handle.children()[2].children()[0].children()[8]
# window_handle.children()[2].children()[0].children()[8].children()[0]
# window_handle.children()[2].children()[0].children()[8].children()[1]
# window_handle.children()[2].children()[0].children()[8].children()[2]
# window_handle.children()[2].children()[0].children()[8].children()[3]
# window_handle.children()[2].children()[0].children()[8].children()[4]


# app = application.Application(backend='uia').start("Spotify")
# print(app)
# app.connect(path="Spotify")
# window_handle = app.top_window()
# window_handle.child_window(auto_id="search-input", control_type="Edit").click()
# window_handle.child_window(title="Search Spotify").click()
# window_handle.child_window(title="Search Spotify").type_keys("Devil")
# print(app)
# Below code clicks
# window_handle.children()[2].children()[0].children()[4].children()[2].children()[0].click()
class SpotifyDesktopApp:

    def __init__(self):
        self.app = None
        self.window_handle = None

    def connect(self):

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
        # window_handle = self.app.top_window()
        # TODO: Needs to add pywinauto wait, otherwise it just fails.
        time.sleep(2)
        self.window_handle.children()[2].children()[0].children()[4].children()[2].children()[0].click()
        self.window_handle.child_window(title="Search Spotify").type_keys(search_for)
        # works until here
        # below is experimental
        print("qq")

    def ui_test_bottom_console(self):
        self.connect()
        time.sleep(2)
        ui_elements_present = []
        # Song Length
        ui_elements_present.append(self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[7].window_text())
        # Time Elapsed timer
        ui_elements_present.append(self.window_handle.children()[2].children()[0].children()[8].children()[1].children()[6].window_text())
        # Repeat Button
        ui_elements_present.append(self.window_handle.child_window(auto_id='player-button-repeat').window_text())
        # Next Button
        ui_elements_present.append(self.window_handle.child_window(auto_id='player-button-next').window_text())
        # Play Button
        ui_elements_present.append(self.window_handle.child_window(auto_id='player-button-play').window_text())
        # Previous Button
        ui_elements_present.append(self.window_handle.child_window(auto_id='player-button-previous').window_text())
        # Shuffle Button
        ui_elements_present.append(self.window_handle.child_window(auto_id='player-button-shuffle').window_text())
        # Currently playing
        ui_elements_present.append(self.window_handle.child_window(auto_id='now-playing-image-large').window_text())
        self.window_handle.close()
        if len(ui_elements_present) == 8:
            return ui_elements_present
        else:
            return "Not all required elements are present"

    def read_songs_from_album(self):
        self.connect()
        songs_in_pl = []
        time.sleep(4)
        playlist_pane = self.window_handle.children()[2].children()[0].children()[1].children()[2]
        time.sleep(2)
        playlist_pane.children()[1].click_input()
        time.sleep(2)
        # Selected playlist pane
        selected_pane = self.window_handle.children()[2].children()[0].children()[5].children()[1].children()[0].children()[6].children()
        for song in selected_pane:
            songs_in_pl.append(song.window_text())
        return songs_in_pl


# SpotifyDesktopApp().search_for_something("Devil")
# print(SpotifyDesktopApp().ui_test_bottom_console())
# print(SpotifyDesktopApp().ui_test_bottom_console())
# SpotifyDesktopApp().read_songs_from_album()
print(SpotifyDesktopApp().ui_test_bottom_console())

# Below: Important, Try to use to get to a unique handle

