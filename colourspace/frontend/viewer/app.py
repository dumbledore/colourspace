# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.av.container import Container
from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.frontend.window.video import VideoFrame


def main():
    app = wx.App()

    container = Container("../data/IMG_5568.MOV")
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

    app.MainLoop()


if __name__ == "__main__":
    main()
