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

        # Initialise the menu
        self.SetMenuBar(self._create_menu())

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

    def _create_menu(self):
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "", "Open a video or an image file")
        file_menu.Append(wx.ID_CLOSE, "Close\tCTRL+W", "Close this file")
        menu_bar.Append(file_menu, "&File")

        edit_menu = wx.Menu()
        seek_time = edit_menu.Append(wx.ID_ANY,
                                     "Seek to time\tCTRL+T", "Seek to a particular time")
        seek_frame = edit_menu.Append(wx.ID_ANY,
                                      "Seek to frame (slow)\tCTRL+F",
                                      "Seek to a particular frame. Can be very slow")
        edit_menu.AppendSeparator()
        edit_menu.Append(wx.ID_SAVE, "", "Save the current frame")
        menu_bar.Append(edit_menu, "&Edit")

        colourspace = wx.Menu()
        self._correction_enabled = colourspace.AppendCheckItem(
            wx.ID_ANY, "Colour Correction\tCTRL+B", "Enable accurate colour representation")

        # On by default
        self._correction_enabled.Check()
        colourspace.AppendSeparator()
        input_colourspace = colourspace.Append(
            wx.ID_ANY, "Input Colourspace\tCTRL+[", "Select input colourspace")
        output_colourspace = colourspace.Append(
            wx.ID_ANY, "Output Colourspace\tCTRL+]", "Select output colourspace")
        menu_bar.Append(colourspace, "&Colourspace")

        view_menu = wx.Menu()
        self._metadata_menu = view_menu.AppendCheckItem(
            wx.ID_ANY, "Metadata Inspector\tCTRL+I", "Show metadata inspector window")
        menu_bar.Append(view_menu, "&View")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "", "About this application")
        menu_bar.Append(help_menu, "&Help")

        # Bind the events
        self.Bind(wx.EVT_MENU, self._on_open_file, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._on_close_file, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self._on_seek_time, seek_time)
        self.Bind(wx.EVT_MENU, self._on_seek_frame, seek_frame)
        self.Bind(wx.EVT_MENU, self._on_save_frame, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self._on_corretion_toggled, self._correction_enabled)
        self.Bind(wx.EVT_MENU, self._on_input_colourspace, input_colourspace)
        self.Bind(wx.EVT_MENU, self._on_output_colourspace, output_colourspace)
        self.Bind(wx.EVT_MENU, self._on_metadata_inspector, self._metadata_menu)
        self.Bind(wx.EVT_MENU, self._on_about, id=wx.ID_ABOUT)

        return menu_bar

    # File
    def _on_open_file(self, event):
        print("open")

    def _on_close_file(self, event):
        print("close")

    # Edit
    def _on_seek_time(self, event):
        print("seek time")

    def _on_seek_frame(self, event):
        print("seek frame")

    def _on_save_frame(self, event):
        print("save")

    # Colourspace
    def _on_corretion_toggled(self, event):
        print(f"correction: {self._correction_enabled.IsChecked()}")

    def _on_input_colourspace(self, event):
        print("input colourspace")

    def _on_output_colourspace(self, event):
        print("output colourspace")

    # View
    def _on_metadata_inspector(self, event):
        print(f"metadata: {self._metadata_menu.IsChecked()}")

    # Help
    def _on_about(self, event):
        message = """
Colourspace is a Python library and viewer tool used to render videos and images in the proper colourspace using the colorspace FFmpeg filter.

It uses the av package to access FFmpeg functionality, and pymediainfo to obtain file and stream metadata, that is not yet available through av (even though it is available in FFmpeg).

Note: PyAV uses a (rather) outdated version of FFmpeg: 5.1.2, which may lack support for some newer stuff. Check the FFmpeg build script for PyAV.

Licensed under BSD 3-Clause.

Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova"""
        wx.MessageDialog(None, message, "About", wx.OK | wx.CENTER | wx.ICON_INFORMATION).ShowModal()
