# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx
from colourspace.av.filter.colourspace import PROFILES, COLOURSPACES, PRIMARIES, TRANSFERS, RANGES


class ColourspaceDialog(wx.Dialog):
    def __init__(self, video, *args, **kw):
        super().__init__(*args, **kw)

        self._video = video
        sizer = wx.BoxSizer(wx.VERTICAL)

        def add_choice(name, choices):
            # label
            label = wx.StaticText(self, label=name)
            sizer.Add(label, 0, wx.ALL, 5)

            # choices
            sizer_ = wx.BoxSizer(wx.HORIZONTAL)

            choices = wx.Choice(self, choices=choices)
            choices.SetSelection(0)
            sizer_.Add(choices, 1, wx.ALL | wx.EXPAND, 5)

            if name == "Primaries":
                profile_warning = wx.StaticText(self, label="\u26A0")
                profile_warning.SetBackgroundColour((255, 255, 0))
                profile_warning.SetForegroundColour((0, 0, 0))
                sizer_.Add(profile_warning, 0, wx.ALL, 5)

            sizer.Add(sizer_, 1, wx.EXPAND, 5)

        add_choice("Profile", list(PROFILES.keys()))
        add_choice("Colour Space", COLOURSPACES)
        add_choice("Primaries", PRIMARIES)
        add_choice("Transfer", TRANSFERS)
        add_choice("Range", ["Ignore"] + RANGES)

        # buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button_ok = wx.Button(self, wx.ID_OK)
        button_ok.SetDefault()
        button_sizer.Add(button_ok, 0, wx.ALL, 5)

        button_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer.Add(button_cancel, 0, wx.ALL, 5)

        button_reset = wx.Button(self, wx.ID_DEFAULT, "Default")
        button_sizer.Add(button_reset, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 1, wx.EXPAND, 5)

        # fix up the frame
        self.SetSizeHints(wx.Size(200, 100), wx.DefaultSize)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.Centre(wx.BOTH)
