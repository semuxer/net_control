import os
import wx
import pygame
from nested_dict import nested_dict
from loguru import logger
from datetime import datetime

from pinger import myping
from config import conf
from texparser import parser
from defaults import *
from version import ver


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(880, 550))

        self.log_last_line_time = datetime(2000, 1, 1, 0, 0, 0)
        self.log_size = 0
        self.log_modification_time = 0

        panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_RICH)
        self.text_ctrl.SetBackgroundColour(wx.BLACK)
        mono_font = wx.Font(10, wx.FONTFAMILY_TELETYPE,
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text_ctrl.SetFont(mono_font)

        self.update_text_ctrl()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_config_info, self.timer)
        # Запускаем таймер с интервалом в 1000 миллисекунд (1 секунда)
        self.timer.Start(1000)
        self.set_win_position(parent)

    def set_win_position(self, parent=None):
        if parent:
            dx, dy = parent.GetSize()
        else:
            dx = 0
            dy = 0
        screenWidth, screenHeight = wx.GetDisplaySize()
        wnWidth, wnHeight = self.GetSize()
        newX = screenWidth - wnWidth - 50 - dx
        newY = screenHeight - wnHeight - 50
        self.SetPosition((newX, newY))

    def update_text_ctrl(self):
        self.text_ctrl.Clear()
        with open(LOGNAME, "r", encoding="utf-8") as f:
            for line in f:
                match = parser(line).getresults()
                if match:
                    level = match.get('level').strip()
                    self.text_ctrl.SetDefaultStyle(
                        wx.TextAttr(wx.LIGHT_GREY))
                    self.text_ctrl.AppendText(match.get('date'))
                    self.text_ctrl.SetDefaultStyle(wx.TextAttr(wx.WHITE))
                    self.text_ctrl.AppendText(" | ")
                    self.text_ctrl.SetDefaultStyle(
                        wx.TextAttr(COLORS.get(level)))
                    self.text_ctrl.AppendText(match.get('level'))
                    self.text_ctrl.SetDefaultStyle(wx.TextAttr(wx.WHITE))
                    self.text_ctrl.AppendText(" | ")

                    if match.get('message'):
                        self.text_ctrl.SetDefaultStyle(
                            wx.TextAttr(COLORS.get(level)))
                        self.text_ctrl.AppendText(match.get('message'))
                        self.text_ctrl.AppendText('\n')
                    if match.get('to'):
                        self.text_ctrl.SetDefaultStyle(
                            wx.TextAttr(wx.WHITE))
                        self.text_ctrl.AppendText(match.get('to'))
                        self.text_ctrl.SetDefaultStyle(
                            wx.TextAttr(COLORS.get(level)))
                        self.text_ctrl.AppendText(match.get('ip'))
                        self.text_ctrl.AppendText('\n')
        self.text_ctrl.ShowPosition(self.text_ctrl.GetLastPosition())

    def get_config_info(self, event):
        log_size = os.path.getsize(LOGNAME)
        log_modification_time = os.path.getmtime(LOGNAME)

        if self.log_size != log_size or self.log_modification_time != log_modification_time:
            self.log_size = log_size
            self.log_modification_time = log_modification_time
            self.update_text_ctrl()


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX & ~(wx.CLOSE_BOX)
        super(MyFrame, self).__init__(parent, title=title, style=style)
        icon = wx.Icon('net24.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.statusbar = self.CreateStatusBar(2)  # Создание панели состояния
        self.statusbar.SetStatusText('  © Movchan Serhii', 0)
        version = ver()
        self.statusbar.SetStatusText(f'  Версія: {version.getver()}', 1)

        self.timer_count = TIMER_DEFAULT

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # panel1 ##################################################################
        panel1 = wx.Panel(main_panel)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.ping = myping(CONFIG)
        self.labels = nested_dict()

        mono_font = wx.Font(8, wx.FONTFAMILY_TELETYPE,
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        for host, data in self.ping.hosts.items():
            st = wx.StaticText(
                panel1,  wx.ID_ANY, label=f"{host.ljust(20)} | {self.ping.hosts[host]['name'].ljust(20)} - {STATUS.get(self.ping.hosts[host]['status'],'')}")
            st.SetFont(mono_font)
            self.labels[host] = st
            vbox.Add(st, 0, wx.ALL, PADDING)

        static_line = wx.StaticLine(
            panel1, wx.ID_ANY, size=(390, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(static_line, 0, wx.ALL, PADDING)
        panel1.SetSizer(vbox)
        vbox.Fit(self)

        # panel2 ##################################################################
        panel2 = wx.Panel(main_panel)
        btn2 = wx.Button(panel2, label='Звіт')
        btn2.Bind(wx.EVT_BUTTON, self.on_open_dialog)

        vbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox2.Add(btn2, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        vbox2.AddStretchSpacer()
        panel2.SetSizer(vbox2)
        vbox2.Fit(self)

        ######################################################
        main_sizer.Add(panel1, 0, wx.TOP | wx.LEFT | wx.RIGHT,
                       10)  # Добавляем панель 1
        main_sizer.Add(panel2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT,
                       10)  # Добавляем панель 1
        main_panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

        ######################################################
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_timer, self.timer)
        # Запускаем таймер с интервалом в 1000 миллисекунд (1 секунда)
        self.timer.Start(200)

        ######################################################

        self.set_win_position()
        self.Show(True)

    def set_win_position(self):
        screenWidth, screenHeight = wx.GetDisplaySize()
        wnWidth, wnHeight = self.GetSize()
        newX = screenWidth - wnWidth - 50
        newY = screenHeight - wnHeight - 50
        self.SetPosition((newX, newY))

    def on_open_dialog(self, event):
        dialog = MyDialog(self, "Звіт")
        dialog.ShowModal()
        dialog.Destroy()

    def update_timer(self, event):
        p = self.ping.get()
        for host, data in self.ping.hosts.items():
            if self.ping.hosts[host]['status'] == 0:
                self.labels[host].SetLabel(
                    f"{host.ljust(20)} | {self.ping.hosts[host]['name'].ljust(20)} - {STATUS.get(self.ping.hosts[host]['status'],'')} ({self.ping.hosts[host]['timecount']})"
                )
            elif self.ping.hosts[host]['status'] == 1:
                self.labels[host].SetLabel(
                    f"{host.ljust(20)} | {self.ping.hosts[host]['name'].ljust(20)} - {STATUS.get(self.ping.hosts[host]['status'],'')} ({self.ping.hosts[host]['timecount']})"
                )

            else:
                self.labels[host].SetLabel(
                    f"{host.ljust(20)} | {self.ping.hosts[host]['name'].ljust(20)} - {STATUS.get(self.ping.hosts[host]['status'],'')} ({self.ping.hosts[host]['timecount']})")


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Перевірка зв'язку")
    app.MainLoop()
    frame.ping.stop()
