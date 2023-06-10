# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx
from colourspace.av.filter.colourspace import PROFILES, COLOURSPACES, PRIMARIES, TRANSFERS, RANGES, Profile


class ColourspaceDialog(wx.Dialog):
    def __init__(self, video, *args, **kw):
        super().__init__(*args, **kw)

        self._video = video
        self._profile = video.input_profile
        self._default_profile, self._profile_errors = Profile.from_stream(video)

        sizer = wx.BoxSizer(wx.VERTICAL)

        def add_choice(name, choices, handler, parent, sizer, error_key=None):
            # label
            label = wx.StaticText(parent, label=name)
            sizer.Add(label, 0, wx.ALL, 5)

            # choices
            sizer_ = wx.BoxSizer(wx.HORIZONTAL)

            choices = wx.Choice(parent, choices=choices)
            choices.SetSelection(0)
            choices.Bind(wx.EVT_CHOICE, handler)
            sizer_.Add(choices, 1, wx.ALL | wx.EXPAND, 5)

            if error_key and (error_key in self._profile_errors):
                profile_warning = wx.StaticText(parent, label="\u26A0")
                profile_warning.SetBackgroundColour((255, 255, 0))
                profile_warning.SetForegroundColour((0, 0, 0))
                profile_warning.SetToolTip(self._profile_errors[error_key])
                sizer_.Add(profile_warning, 0, wx.ALL, 5)

            sizer.Add(sizer_, 0, wx.EXPAND, 5)

            return choices

        self._profiles = add_choice("Profile", ["Custom"] + list(PROFILES.keys()),
                                    self._on_profile, self, sizer, "profile")

        advanced = wx.CollapsiblePane(self, wx.ID_ANY, "Advanced", wx.DefaultPosition,
                                      wx.DefaultSize, wx.CP_DEFAULT_STYLE)
        advanced.Collapse(self._profile.name != "Custom")
        sizer_advanced = wx.BoxSizer(wx.VERTICAL)

        self._colourspaces = add_choice("Colour Space", COLOURSPACES,
                                        self._on_colourspace, advanced.GetPane(), sizer_advanced, "colourspace")
        self._primaries = add_choice("Primaries", PRIMARIES, self._on_primaries,
                                     advanced.GetPane(), sizer_advanced, "primaries")
        self._transfers = add_choice("Transfer", TRANSFERS, self._on_transfer,
                                     advanced.GetPane(), sizer_advanced, "transfer")
        self._ranges = add_choice("Range", ["Ignore"] + RANGES, self._on_range,
                                  advanced.GetPane(), sizer_advanced, "range")

        advanced.GetPane().SetSizer(sizer_advanced)
        advanced.GetPane().Layout()
        sizer_advanced.Fit(advanced.GetPane())
        sizer.Add(advanced, 1, wx.EXPAND | wx.ALL, 5)

        # buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button_ok = wx.Button(self, wx.ID_OK)
        button_ok.SetDefault()
        button_sizer.Add(button_ok, 0, wx.ALL, 5)

        button_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer.Add(button_cancel, 0, wx.ALL, 5)

        button_reset = wx.Button(self, wx.ID_DEFAULT, "Default")
        button_sizer.Add(button_reset, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.EXPAND, 5)

        self._update_from_profile()

        # fix up the frame
        self.SetSizeHints(wx.Size(200, 100), wx.DefaultSize)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.Centre(wx.BOTH)

    def _update_from_profile(self):
        # Profile name
        idx = self._profiles.FindString(self._profile.name)
        self._profiles.SetSelection(idx)

        # Colourspace
        idx = self._colourspaces.FindString(self._profile.colourspace)
        self._colourspaces.SetSelection(idx)

        # Primaries
        idx = self._primaries.FindString(self._profile.primaries)
        self._primaries.SetSelection(idx)

        # Transfer characteristic
        idx = self._transfers.FindString(self._profile.transfer)
        self._transfers.SetSelection(idx)

        # Range
        idx = self._ranges.FindString(self._profile.range) if self._profile.range else 0
        self._ranges.SetSelection(idx)

    def _on_profile(self, event):
        print("on profile")

    def _on_colourspace(self, event):
        print("on csp")

    def _on_primaries(self, event):
        print("on primaries")

    def _on_transfer(self, event):
        print("on trc")

    def _on_range(self, event):
        print("on range")