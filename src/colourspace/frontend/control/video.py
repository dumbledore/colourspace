# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx
import wx.lib.newevent

from colourspace.frontend.util.pil import image_to_bitmap
from PIL import Image

VideoSeekEvent, EVT_VIDEO_SEEK = wx.lib.newevent.NewEvent()


class VideoPanel(wx.Panel):
    # A spacer between the video panel and the slider
    # W/o the spacer, a portion of the video panel
    # has to be re-painted while moving the slider.
    SPACER = 4

    def __init__(self, parent,
                 video,
                 resize_quality=Image.LINEAR,
                 initial_min_max_size=(320, 640),
                 *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._video = video
        self._resize_quality = resize_quality

        # calculate appropriate initial size for the video panel
        video_size = (video.width, video.height)
        initial_min, initial_max = initial_min_max_size

        if max(video_size) > initial_max:
            divisor = max(video_size) // initial_max
            video_size = [s // divisor for s in video_size]
        elif max(video_size) < initial_min:
            multiplier = initial_min // max(video_size)
            print(multiplier)
            video_size = [s * multiplier for s in video_size]

        video_size = self.FromDIP(video_size)

        self._frame = video.frame.to_image()

        self._panel = wx.Panel(self, size=video_size,
                               style=wx.FULL_REPAINT_ON_RESIZE)
        self._panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self._panel.Bind(wx.EVT_PAINT, self._on_paint)

        duration = int(video.duration * 1000)  # in ms

        if video.container.seekable:
            self._slider = wx.Slider(
                self, maxValue=duration, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
            self._slider.ClearTicks()
            for pts in video.key_frames:
                self._slider.SetTick(int(pts * 1000))

            self._slider.Bind(wx.EVT_SLIDER, self._on_seek)
        else:
            self._slider = None

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._panel, 1, wx.EXPAND)

        if self._slider:
            sizer.AddSpacer(VideoPanel.SPACER)
            sizer.Add(self._slider, 0, wx.EXPAND)

        self.SetSizerAndFit(sizer)

    @property
    def video(self):
        return self._video

    def _on_paint(self, event):
        # Context for drawing into the frame
        dc = wx.AutoBufferedPaintDCFactory(self._panel)

        # Scale the frame
        frame = self._frame.resize(
            self._panel.GetClientSize(), self._resize_quality)

        # Convert from PIL image to wx.Bitmap
        bitmap = image_to_bitmap(frame)

        # Draw to frame
        dc.DrawBitmap(bitmap, 0, 0)

    def _on_seek(self, event):
        position = event.GetInt() / 1000

        # Repaint only if seek actually
        # produced a different frame
        if self._video.seek(position):
            # update the current frame
            self._frame = self._video.frame.to_image()
            event = VideoSeekEvent(position=position)
            wx.PostEvent(self.Parent, event)
            self._panel.Refresh()

    def get_best_size(self, size):
        aspect_ratio = self.video.height / self.video.width
        width, height = size
        height = int(width * aspect_ratio)

        if self._slider:
            height += VideoPanel.SPACER
            height += self._slider.GetClientSize()[1]

        return (width, height)