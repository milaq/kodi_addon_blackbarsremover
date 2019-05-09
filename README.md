![](resources/icon.png)

# Introduction

Black Bars Remover is a simple addon for Kodi which allows you to scale/fit the playing video to your screen height,
eliminating all black bars.
This also takes Kodi's "minimise black bars" setting into consideration. It only zooms the correct amount without
overscaling.

# Installation

Go to the releases page and download an addon zip or get the [master branch](https://github.com/milaq/kodi_addon_blackbarsremover/archive/master.zip)
version and place it on your Kodi machine. You can then install it by using the "install from zip file" option.

# Usage

You can easily map the script to one of your remote buttons by modifying/creating
`.kodi/userdata/keymaps/keyboard.xml`.

E.g. to have the script run on pressing the "Record" button:
```
<keymap>
  <FullscreenVideo>
    <remote>
      <record>RunScript(script.video.blackbarsremover,0)</record>
    </remote>
  </FullscreenVideo>
</keymap>
```

See [the keymap section in the Kodi wiki](https://kodi.wiki/view/Keymap) for more info.
