# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.frontend.control.video import VideoPanel
from PIL import Image


class VideoFrame(wx.Frame):
    def __init__(self, video,
                 resize_quality=Image.LINEAR,
                 size_divisor=640,
                 *args, **kwargs):

        super().__init__(None, title=video.container.filename, *args, **kwargs)

        self._statusbar = self.CreateStatusBar(2)
        self._video = VideoPanel(self, video, resize_quality, size_divisor)
        self.Fit()

        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_SIZE, self._on_size)

    def _on_close(self, event):
        # close the container w/o waiting for dtr
        self._video.video.container.close()

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_size(self, event):
        size = self.GetClientSize()
        size = self._video.get_best_size(size)
        self.SetClientSize(size)
        event.Skip()
