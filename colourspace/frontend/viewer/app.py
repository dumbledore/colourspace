# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.av.container import Container
from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, PROFILES
from colourspace.frontend.window.video import VideoFrame


def main():
    app = wx.App()

    container = Container("../data/IMG_5568.MOV")
    stream = container.streams[0]

    filter = ColourspaceFilter(PROFILES["bt2020"], PROFILES["bt709"])
    stream = FilteredStream(stream, [filter])
    frame = VideoFrame(stream)
    frame.Center()
    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
