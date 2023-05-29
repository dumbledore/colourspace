# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import sys
import wx

from colourspace.av.container import Container
from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.frontend.window.video import VideoFrame


class App(wx.App):
    def Open(self, filename=None):
        stream = None

        if filename:
            filename = os.path.abspath(filename)

            # Is this already opened?
            if filename in self._opened:
                frame = self._opened[filename]
                frame.Raise()
                return frame

            # Try opening a new one
            try:
                container = Container(filename)
                stream = container.streams[0]

                stream_profile, profile_errors = Profile.from_stream(stream)
                if profile_errors:
                    print(profile_errors)
                print(f"Selected input profile: {stream_profile}")
                filter = ColourspaceFilter(stream_profile, PROFILES["bt709"])
                stream = FilteredStream(stream, [filter])
            except Exception as e:
                wx.MessageDialog(None, f"Failed to open '{os.path.basename(filename)}: {e}'",
                                 "Failed to open file", wx.OK | wx.CENTER | wx.ICON_ERROR).ShowModal()
                return None

        frame = VideoFrame(self, stream)
        frame.Center()
        frame.Show()
        self._opened[filename] = frame
        return frame

    def OnInit(self):
        self._opened = {}
        return True


def main():
    app = App()

    if sys.argv[1:]:
        # Open all files passed by command line
        for filename in sys.argv[1:]:
            app.Open(filename)
    else:
        # No args specified, open an empty window
        app.Open()

    app.MainLoop()


if __name__ == "__main__":
    main()
