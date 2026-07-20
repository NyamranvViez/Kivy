[app]
title = Bible Myanmar
package.name = biblemyanmar
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json,db
version = 1.5

# အစ်ကို ထည့်ထားတဲ့ ပုံလမ်းကြောင်းများ
icon.filename = %(source.dir)s/app_icon.png
presplash.filename = %(source.dir)s/app_icon.png

# ကွန်ရက်ပတ်သက်တာတွေ မလိုအောင် pillow သေချာထည့်ပေးထားပါတယ် (kivy version ကို pin ထားပါတယ်)
requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# SDK License များကို အလိုအလျောက် လက်ခံရန်
android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
[buildozer]
log_level = 2
warn_on_root = 1
