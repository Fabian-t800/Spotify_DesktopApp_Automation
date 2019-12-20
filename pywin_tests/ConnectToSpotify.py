from pywinauto import application
from robot.api import logger as robologger
import pywinauto
import psutil


class ConnectToSpotify:

    def __init__(self):
        self.app = None
        self.window_handle = None
        if self.connect() is None:
            self.connect()
            robologger.warn("ConnectToSpotify's constructor has been used.")


    def connect(self):

        if self.is_process() is True:
            spotify_pids = []
            if self.is_process() is True:
                for proc in psutil.process_iter():
                    if proc.name() == "Spotify.exe":
                        spotify_pids.append(proc.pid)
                for spotify_pid in spotify_pids:
                    try:
                        self.app = pywinauto.application.Application(backend='uia').connect(process=spotify_pid)
                        robologger.warn("Connect to a process branch has been chosen.")
                        try:
                            self.app.windows()[0].maximize()
                            return self.app.top_window(), True
                        except IndexError:
                            continue
                    except RuntimeError:
                        raise RuntimeError(f"The expected result was to connect to the {spotify_pid}. Instead it could not.")

        else:
            self.app = application.Application(backend='uia', allow_magic_lookup=True).start("Spotify")
            self.app.connect(path="Spotify")
            return self.app.top_window(), True

    def is_process(self):
        for proc in psutil.process_iter():
            if proc.name() == "Spotify.exe":
                return True
            else:
                return False


class SingleConnect:
    __instance = None
    @staticmethod
    def get_connection_instance():
        if SingleConnect.__instance is None:
            SingleConnect()
        return SingleConnect.__instance

    def __init__(self):
        if SingleConnect.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SingleConnect.__instance = self

