[app]
title = Myanmar and Ethnic Bibles
package.name = myanmarandethnicbibles
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,xml,atlas,ttf,txt,json,db
version = 1.5

icon.filename = %(source.dir)s/app_icon.png
presplash.filename = %(source.dir)s/splash.png
android.presplash_color = #FFFFFF

requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
[buildozer]
log_level = 2
warn_on_root = 1
