import sys
import math

import json
import xbmc
import xbmcaddon
import xbmcgui

from lib.player import Player

LOG_TAG = "BlackBarsRemover"

addon = xbmcaddon.Addon()


def log(msg, level):
    xbmc.log("%s: %s" % (LOG_TAG, msg), level=level)

def notify(text, seconds=None):
    if seconds:
        xbmc.executebuiltin('Notification(' + addon.getAddonInfo('name') + ', ' + text + ', ' + str(seconds * 1000) + ')')
    else:
        xbmc.executebuiltin('Notification(' + addon.getAddonInfo('name') + ', ' + text + ')')

def get_current_zoom_level():
    result_raw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetViewMode", "id": 1}')
    result_json = json.loads(unicode(result_raw, 'utf-8'))
    if 'result' in result_json and 'zoom' in result_json['result']:
        zoom = float("{:.2f}".format(result_json['result']['zoom']))
        return zoom
    log("Couldn't get zoom level properties, assuming no zoom", xbmc.LOGWARNING)
    return 1.0

def apply_zoom(level):
    result_raw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.SetViewMode", "params": {"viewmode": {"zoom": ' + str(level) + ' }}, "id": 1}')
    result_json = json.loads(unicode(result_raw, 'utf-8'))
    if 'result' in result_json and result_json['result'] == 'OK':
        return True
    return False

def get_desired_zoom_level():
    blackbarcomp = None
    blackbarcomp_raw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "videoplayer.errorinaspect"}, "id": 1}')
    blackbarcomp_json = json.loads(unicode(blackbarcomp_raw, 'utf-8'))
    if 'result' in blackbarcomp_json:
        if 'value' in blackbarcomp_json['result']:
            blackbarcomp = int(blackbarcomp_json['result']['value'])
    if blackbarcomp is None:
        return 0
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
    return zoomlevel

def get_new_zoom_supported():
    version_raw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    version_json = json.loads(unicode(version_raw, 'utf-8'))
    if not version_json.has_key('result') and not version_json['result'].has_key('version'):
        return False
    if version_json['result']['version']['major'] > 18:
        return True
    if version_json['result']['version']['major'] == 18 and version_json['result']['version']['minor'] >= 2:
        return True
    return False


if not get_new_zoom_supported():
    notify(addon.getLocalizedString(30005) + ": 18.2", 10)
    sys.exit(1)

monitor = xbmc.Monitor()
player = Player()
dialog = xbmcgui.Dialog()
while not monitor.abortRequested():
    if monitor.waitForAbort(2):
        break
    if player.isPlaying():
        last_file = player.getLastFile()
        try:
            current_file = player.getPlayingFile()
        except Exception as e:
            player.setPlaying(False)
            continue
        if last_file is None or last_file != current_file:
            log("New video now playing", xbmc.LOGDEBUG)
            player.setLastFile(current_file)
            zoomlevel = get_desired_zoom_level()
            if zoomlevel == 0:
                log("Could not determine black bar compensation", xbmc.LOGERROR)
                notify(addon.getLocalizedString(30003))
                continue
            log("Desired zoom level: %f" % zoomlevel, xbmc.LOGDEBUG)
            if zoomlevel <= 1.0:
                log("No zoom adjustment necessary", xbmc.LOGNOTICE)
                continue
            zoomlevel_current = get_current_zoom_level()
            log("Current zoom level: %f" % zoomlevel_current, xbmc.LOGDEBUG)
            if zoomlevel_current == zoomlevel:
                log("Already got correct zoomlevel", xbmc.LOGNOTICE)
                continue
            if apply_zoom(zoomlevel):
                log("Applied zoom level successfully", xbmc.LOGNOTICE)
                notify(addon.getLocalizedString(30001) + " (" + str(int((zoomlevel - 1.0) * 100.0)) + "%)")
            else:
                log("Could not apply zoom", xbmc.LOGERROR)
                notify(addon.getLocalizedString(30004))
