# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.av.container import Container
from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.frontend.window.video import VideoFrame


class App(wx.App):
    def Open(self, filename=None):
        stream = None

        if filename:
            container = Container(filename)
            stream = container.streams[0]

            stream_profile, profile_errors = Profile.from_stream(stream)
            if profile_errors:
                print(profile_errors)
            print(f"Selected input profile: {stream_profile}")
            filter = ColourspaceFilter(stream_profile, PROFILES["bt709"])
            stream = FilteredStream(stream, [filter])

        frame = VideoFrame(stream)
        frame.Center()
        frame.Show()

    def OnInit(self):
        self.Open("../../data/IMG_5568.MOV")
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    main()
