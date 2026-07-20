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

# ကွန်ရက်ပတ်သက်တာတွေ မလိုအောင် pillow သေချာထည့်ပေးထားပါတယ်
requirements = python3, kivy, pillow

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1