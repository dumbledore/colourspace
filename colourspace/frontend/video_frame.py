# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

from PIL import Image


class VideoFrame(wx.Frame):
    def __init__(self, video,
                 resize_quality=Image.LINEAR,
                 size_divisor=640,
                 *args, **kwargs):

        super().__init__(None, title=video.container.filename, *args, **kwargs)

        self._video = video
        self._screen_size = (video.width, video.height)
        self._screen_aspect = video.width / video.height
        self._resize_quality = resize_quality

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.SetClientSize(self.FromDIP(self.choose_size(size_divisor)))

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.statusbar = self.CreateStatusBar(2)

    def choose_size(self, size_divisor):
        size = self._screen_size
        divisor = max(size) // size_divisor
        return [s // divisor for s in size]

    def on_size(self, event):
        width, _ = self.GetClientSize()
        size = (width, int(width / self._screen_aspect))

        if self.GetClientSize() != size:
            self.SetClientSize(size)

    def on_paint(self, event):
        # Context for drawing into the frame
        dc = wx.AutoBufferedPaintDC(self)

        # Obtain current frame
        frame = self._video.frame

        # Convert it to PIL image
        frame = frame.to_image()

        # Scale the frame
        frame = frame.resize(self.GetClientSize(), self._resize_quality)

        # Convert from PIL image to wx.Bitmap
        bitmap = wx.Bitmap.FromBuffer(*frame.size, frame.tobytes())

        # Draw to frame
        dc.DrawBitmap(bitmap, 0, 0)

    def on_close(self, event):
        # close the container w/o waiting for dtr
        self._video.container.close()

        event.Skip()
