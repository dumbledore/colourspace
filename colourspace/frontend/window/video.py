# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.frontend.control.video import VideoPanel
from PIL import Image


class VideoFrame(wx.Frame):
    def __init__(self, video=None,
                 resize_quality=Image.LINEAR,
                 size_divisor=640,
                 *args, **kwargs):

        title = video.container.filename if video else "Untitled"
        super().__init__(None, title=title, *args, **kwargs)

        self._statusbar = self.CreateStatusBar(2)

        if video:
            self._has_video = True
            self._video = VideoPanel(self, video, resize_quality, size_divisor)
        else:
            self._has_video = False
            size = self.FromDIP((640, 480))
            self._video = wx.Panel(self, size=size)

        self.Fit()

        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_SIZE, self._on_size)

    def _on_close(self, event):
        if self._has_video:
            # close the container w/o waiting for dtr
            self._video.video.container.close()

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_size(self, event):
        if self._has_video:
            size = self.GetClientSize()
            size = self._video.get_best_size(size)
            self.SetClientSize(size)

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()
