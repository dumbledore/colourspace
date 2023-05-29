# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx


class Drop(wx.FileDropTarget):
    def __init__(self, app):
        super().__init__()
        self._app = app

    def OnDropFiles(self, x, y, filenames):
        for filename in filenames:
            self._app.Open(filename)

        return True
