# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from colourspace.frontend.utils.pil import image_to_bitmap
from PIL import Image


class VideoPanel(wx.Panel):
    # A spacer between the video panel and the slider
    # W/o the spacer, a portion of the video panel
    # has to be re-painted while moving the slider.
    SPACER = 4

    def __init__(self, parent,
                 video,
                 resize_quality=Image.LINEAR,
                 size_divisor=640,
                 *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._video = video
        self._resize_quality = resize_quality

        # calculate appropriate initial size for the video panel
        video_size = (video.width, video.height)
        divisor = max(video_size) // size_divisor
        video_size = [s // divisor for s in video_size]
        video_size = self.FromDIP(video_size)

        self._panel = wx.Panel(self, size=video_size)
        self._panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self._panel.Bind(wx.EVT_PAINT, self.on_paint)

        duration = int(video.duration * 1000)  # in ms
        self._slider = wx.Slider(self, maxValue=duration)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._panel, 1, wx.EXPAND)
        sizer.AddSpacer(VideoPanel.SPACER)
        sizer.Add(self._slider, 0, wx.EXPAND)
        self.SetSizerAndFit(sizer)

    @property
    def video(self):
        return self._video

    def on_paint(self, event):
        # Context for drawing into the frame
        dc = wx.AutoBufferedPaintDC(self._panel)

        # Obtain current frame
        frame = self._video.frame

        # Convert it to PIL image
        frame = frame.to_image()

        # Scale the frame
        frame = frame.resize(self._panel.GetClientSize(), self._resize_quality)

        # Convert from PIL image to wx.Bitmap
        bitmap = image_to_bitmap(frame)

        # Draw to frame
        dc.DrawBitmap(bitmap, 0, 0)

    def get_best_size(self, size):
        aspect_ratio = self.video.height / self.video.width
        width, height = size
        height = int(width * aspect_ratio)
        height += VideoPanel.SPACER
        height += self._slider.GetClientSize()[1]

        return (width, height)
