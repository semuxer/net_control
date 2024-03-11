import wx

CONFIG = "config.json"
TIMER_DEFAULT = 5
PADDING = 2
LOGNAME = "report.log"
LOGDTFORMAT = '%Y-%m-%d %H:%M:%S'
LOGGERFORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {level} | {message}"
LOGGERLEVEL = "INFO"
LOGGERSIZE = "1 MB"
COLORS = {
    "BLACK": wx.BLACK,
    "TRACE": wx.WHITE,
    "WHITE": wx.WHITE,
    "ERROR": wx.RED,
    "CRITICAL": wx.RED,
    "SUCCESS": wx.GREEN,
    "BLUE": wx.BLUE,
    "CYAN": wx.CYAN,
    "WARNING": wx.YELLOW,
    "INFO": wx.LIGHT_GREY,
    "DEBUG": wx.LIGHT_GREY,
    "LIGHT_GREY": wx.LIGHT_GREY,
}

STATUS = {
    0: "OK",
    1: "BAD",
    2: "wait",
}
