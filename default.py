import sys
import math

import json
import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()


def notify(text):
    xbmc.executebuiltin('Notification(' + addon.getAddonInfo('name') + ', ' + text + ')')


def apply_zoom_legacy(level):
    steps = int((level * 100.0) - 100)
    for _ in range(0, steps):
        xbmc.executebuiltin('Action(ZoomIn)')


blackbarcomp = None
blackbarcomp_raw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "videoplayer.errorinaspect"}, "id": 1}')
blackbarcomp_json = json.loads(unicode(blackbarcomp_raw, 'utf-8'))
if 'result' in blackbarcomp_json:
    if 'value' in blackbarcomp_json['result']:
        blackbarcomp = int(blackbarcomp_json['result']['value'])

if not blackbarcomp:
    notify(addon.getLocalizedString(30003))
    sys.exit(1)

aspectratio_screen = float(xbmcgui.getScreenWidth()) / float(xbmcgui.getScreenHeight())
aspectratio_video = xbmc.RenderCapture().getAspectRatio()
aspectratio_compensation = aspectratio_video - (aspectratio_video * (blackbarcomp / 100.0))
ratio_correction = (aspectratio_compensation / aspectratio_screen)
zoomlevel = math.ceil(ratio_correction * 100.0) / 100.0

user_compensation = int(addon.getSetting('user_compensation'))
zoomlevel = zoomlevel + (user_compensation / 100.0)

maximum_zoom_level = float(1.0 + int(addon.getSetting('maximum_compensation')) / 100.0)
if zoomlevel > maximum_zoom_level:
    zoomlevel = maximum_zoom_level

if zoomlevel <= 1.0:
    notify(addon.getLocalizedString(30002))
    sys.exit(1)

notify(addon.getLocalizedString(30001) + " (" + str(int((zoomlevel - 1.0) * 100.0)) + "%)")
apply_zoom_legacy(zoomlevel)
