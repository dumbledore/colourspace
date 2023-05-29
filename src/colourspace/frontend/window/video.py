# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.frontend.control.video import VideoPanel, EVT_VIDEO_SEEK
from colourspace.frontend.util.drop import Drop
from colourspace.util.time import time_format
from PIL import Image


class VideoFrame(wx.Frame):
    def __init__(self, app, video=None,
                 resize_quality=Image.LINEAR,
                 initial_min_max_size=(320, 640),
                 *args, **kwargs):

        title = video.container.filename if video else "Untitled"
        super().__init__(None, title=title, *args, **kwargs)

        self._app = app
        self._statusbar = self.CreateStatusBar(2)

        if video:
            self._has_video = True
            self._video = VideoPanel(self, video, resize_quality, initial_min_max_size)
        else:
            self._has_video = False
            size = self.FromDIP((640, 480))
            self._video = wx.Panel(self, size=size)

        # Set current video position in the status bar to 00:00:00
        self._update_video_position(0)

        self.Fit()

        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(EVT_VIDEO_SEEK, self._on_video_seek)
        self.SetDropTarget(Drop(app))

    def _on_close(self, event):
        if self._has_video:
            # close the container w/o waiting for dtr
            filename = self._video.video.container.filename
            self._video.video.container.close()
            self._app.OnCloseWindow(filename)

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_size(self, event):
        if self._has_video:
            size = self.GetClientSize()
            size = self._video.get_best_size(size)
            self.SetClientSize(size)

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_video_seek(self, event):
        self._update_video_position(event.position)

    def _update_video_position(self, position):
        position = time_format(position)
        duration = time_format(
            self._video.video.duration if self._has_video else 0)
        self._statusbar.SetStatusText(position + "/" + duration)
