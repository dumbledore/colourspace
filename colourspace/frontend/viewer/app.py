# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.av.container import Container
from colourspace.frontend.window.video_frame import VideoFrame


def main():
    app = wx.App()

    container = Container("../data/IMG_5568.MOV")
    frame = VideoFrame(container.streams[0])
    frame.Center()
    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
