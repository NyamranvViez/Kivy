import os
import json
import xml.etree.ElementTree as ET
import threading
import time

from kivy.utils import platform
if platform == 'android':
    os.environ['KIVY_TEXT'] = 'pango'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.splitter import Splitter  
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.clock import Clock

DEFAULT_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pyidaungsu.ttf")

FONT_MAP = {
    "BurmeseBible": "Pyidaungsu.ttf",
    "ShanBible": "Pyidaungsu.ttf",            
    "HindiBible": "NotoSansDevanagari-Regular.ttf",
    "HebrewBible": "NotoSansHebrew-Regular.ttf",
    "EnglishBible": "Pyidaungsu.ttf"
}

def get_font_for_version(version_name):
    font_file = FONT_MAP.get(version_name, "Pyidaungsu.ttf")
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_file)
    if os.path.exists(font_path):
        return font_path
    return DEFAULT_FONT if os.path.exists(DEFAULT_FONT) else None

BIBLE_BOOKS = {
    "1": "Genesis", "2": "Exodus", "3": "Leviticus", "4": "Numbers", "5": "Deuteronomy",
    "6": "Joshua", "7": "Judges", "8": "Ruth", "9": "1 Samuel", "10": "2 Samuel",
    "11": "1 Kings", "12": "2 Kings", "13": "1 Chronicles", "14": "2 Chronicles", "15": "Ezra",
    "16": "Nehemiah", "17": "Esther", "18": "Job", "19": "Psalms", "20": "Proverbs",
    "21": "Ecclesiastes", "22": "Song of Solomon", "23": "Isaiah", "24": "Jeremiah", "25": "Lamentations",
    "26": "Ezekiel", "27": "Daniel", "28": "Hosea", "29": "Joel", "30": "Amos",
    "31": "Obadiah", "32": "Jonah", "33": "Micah", "34": "Nahum", "35": "Habakkuk",
    "36": "Zephaniah", "37": "Haggai", "38": "Zechariah", "39": "Malachi", "40": "Matthew",
    "41": "Mark", "42": "Luke", "43": "John", "44": "Acts", "45": "Romans",
    "46": "1 Corinthians", "47": "2 Corinthians", "48": "Galatians", "49": "Ephesians", "50": "Philippians",
    "51": "Colossians", "52": "1 Thessalonians", "53": "2 Thessalonians", "54": "1 Timothy", "55": "2 Timothy",
    "56": "Titus", "57": "Philemon", "58": "Hebrews", "59": "James", "60": "1 Peter",
    "61": "2 Peter", "62": "1 John", "63": "2 John", "64": "3 John", "65": "Jude",
    "66": "Revelation"
}

BURMESE_BOOKS = {
    "Genesis": "ကမ္ဘာဦးကျမ်း", "Exodus": "ထွက်မြောက်ရာကျမ်း", "Leviticus": "ဝတ်ပြုရာကျမ်း", "Numbers": "တောလည်ရာကျမ်း", "Deuteronomy": "တရားဟောရာကျမ်း",
    "Joshua": "ယောရှုမှတ်တမ်း", "Judges": "တရားသူကြီးမှတ်တမ်း", "Ruth": "ရုသဝတ္ထု", "1 Samuel": "ဓမ္မရာဇဝင်ပထမစောင်", "2 Samuel": "ဓမ္မရာဇဝင်ဒုတိယစောင်",
    "1 Kings": "ဓမ္မရာဇဝင်တတိယစောင်", "2 Kings": "ဓမ္မရာဇဝင်စတုတ္ထစောင်", "1 Chronicles": "ရာဇဝင်ချုပ်ပထမစောင်", "2 Chronicles": "ရာဇဝင်ချုပ်ဒုတိယစောင်", "Ezra": "ဧဇရမှတ်တမ်း",
    "Nehemiah": "နေဟမိမှတ်တမ်း", "Esther": "ဧသတာဝတ္ထု", "Job": "ယောဘဝတ္ထု", "Psalms": "ဆာလံကျမ်း", "Proverbs": "သုတ္တံကျမ်း",
    "Ecclesiastes": "ဒေသနာကျမ်း", "Song of Solomon": "ရှောလမုန်သီချင်း", "Isaiah": "ဟေရှာယအနာဂတ္တိကျမ်း", "Jeremiah": "ယေရမိအနာဂတ္တိကျမ်း", "Lamentations": "ယေရမိမြည်တမ်းစောင်",
    "Ezekiel": "ယေဇကျေလအနာဂတ္တိကျမ်း", "Daniel": "ဒံယေလအနာဂတ္တိကျမ်း", "Hosea": "ဟောရှေအနာဂတ္တိကျမ်း", "Joel": "ယောလအနာဂတ္တိကျမ်း", "Amos": "အာမုတ်အနာဂတ္တိကျမ်း",
    "Obadiah": "ဩဗဒိအနာဂတ္တိကျမ်း", "Jonah": "ယောနဝတ္ထု", "Micah": "မိက္ခာအနာဂတ္တိကျမ်း", "Nahum": "နာဟုံအနာဂတ္တိကျမ်း", "Habakkuk": "ဟဗက္ကုက်အနာဂတ္တိကျမ်း",
    "Zephaniah": "ဇေဖနိအနာဂတ္တိကျမ်း", "Haggai": "ဟဂ္ဂဲအနာဂတ္တိကျမ်း", "Zechariah": "ဇာခရိအနာဂတ္တိကျမ်း", "Malachi": "မာလခိအနာဂတ္တိကျမ်း", "Matthew": "ရှင်မဿဲခရစ်ဝင်",
    "Mark": "ရှင်မာကုခရစ်ဝင်", "Luke": "ရှင်လုကာခရစ်ဝင်", "John": "ရှင်ယောဟန်ခရစ်ဝင်", "Acts": "တမန်တော်ဝတ္ထု", "Romans": "ရောမသြဝါဒစာ",
    "1 Corinthians": "ကောရိန္သုပထမစောင်", "2 Corinthians": "ကောရိန္သုဒုတိယစောင်", "Galatians": "ဂလာတိစာ", "Ephesians": "ဧဖက်စာ", "Philippians": "ဖိလိပ္ပိစာ",
    "Colossians": "ကောလောသဲစာ", "1 Thessalonians": "သက်သာလောနိတ်ပထမစောင်", "2 Thessalonians": "သက်သာလောနိတ်ဒုတိယစောင်", "1 Timothy": "တိမောသေပထမစောင်", "2 Timothy": "တိမောသေဒုတိယစောင်",
    "Titus": "တိတုစာ", "Philemon": "ဖိလေမုန်စာ", "Hebrews": "ဟေဗြဲစာ", "James": "ယာကုပ်စာ", "1 Peter": "ပေတရုပထမစောင်",
    "2 Peter": "ပေတရုဒုတိယစောင်", "1 John": "ယောဟန်ပထမစောင်", "2 John": "ယောဟန်ဒုတိယစောင်", "3 John": "ယောဟန်တတိယစောင်", "Jude": "ယုဒစာ",
    "Revelation": "ဗျာဒိတ်ကျမ်း"
}

OT_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

NT_BOOKS = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

class VerseItem(ButtonBehavior, BoxLayout):
    def __init__(self, verse_num, verse_text, app_ref, is_dark_mode=False, font_name=None, is_highlighted=False, **kwargs):
        super(VerseItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = [dp(15), dp(8), dp(15), dp(8)]
        
        self.verse_num = verse_num
        self.verse_text = verse_text
        self.app_ref = app_ref
        self.is_selected = False
        self.is_highlighted = is_highlighted
        
        self.apply_theme_colors(is_dark_mode)

        with self.canvas.before:
            self.bg_color = Color(*self.default_bg) 
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        cleaned_text = " ".join(verse_text.split())
        self.lbl = Label(
            text=f"[b]{verse_num}.[/b] {cleaned_text}",
            markup=True,
            color=self.text_color,
            font_name=font_name if font_name else DEFAULT_FONT,
            size_hint_y=None,
            halign='left',
            valign='middle',
            font_size='16sp',
            line_height=1.4
        )
        self.add_widget(self.lbl)
        self.update_bg_color()

    def on_size(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        self.lbl.text_size = (max(dp(100), self.width - dp(30)), None)
        self.lbl.texture_update()
        self.lbl.height = self.lbl.texture_size[1]
        self.height = max(dp(36), self.lbl.height + dp(16))

    def on_pos(self, *args):
        self.bg_rect.pos = self.pos

    def update_bg_color(self):
        if self.is_selected:
            self.bg_color.rgba = self.selected_bg
        elif self.is_highlighted:
            self.bg_color.rgba = self.highlight_bg
        else:
            self.bg_color.rgba = self.default_bg

    def on_press(self):
        self.is_selected = not self.is_selected
        self.update_bg_color()
        if self.is_selected:
            self.app_ref.add_selected_verse(self.verse_num, self.verse_text)
        else:
            self.app_ref.remove_selected_verse(self.verse_num)

    def apply_theme_colors(self, is_dark_mode):
        self.default_bg = [0.06, 0.09, 0.14, 1] if is_dark_mode else [1, 1, 1, 1]
        self.selected_bg = [0.2, 0.4, 0.7, 1] if is_dark_mode else [0.8, 0.9, 1.0, 1] 
        self.highlight_bg = [0.4, 0.4, 0.1, 1] if is_dark_mode else [1.0, 0.95, 0.6, 1] 
        self.text_color = [0.9, 0.95, 1, 1] if is_dark_mode else [0, 0, 0, 1]
        
        if hasattr(self, 'lbl'):
            self.lbl.color = self.text_color
            self.update_bg_color()

class BiblePageLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BiblePageLayout, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = dp(2)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

class SwipeableScrollView(ScrollView):
    def __init__(self, app_ref=None, **kwargs):
        super(SwipeableScrollView, self).__init__(**kwargs)
        self.app_ref = app_ref

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.ud['swipe_start_x'] = touch.x
            touch.ud['swipe_start_y'] = touch.y
        return super(SwipeableScrollView, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if 'swipe_start_x' in touch.ud and self.collide_point(*touch.pos):
            dx = touch.x - touch.ud['swipe_start_x']
            dy = touch.y - touch.ud['swipe_start_y']
            if abs(dx) > dp(50) and abs(dx) > abs(dy) * 2:
                if self.app_ref:
                    if dx > 0:
                        self.app_ref.navigate_chapter("prev")
                    else:
                        self.app_ref.navigate_chapter("next")
                return True 
        return super(SwipeableScrollView, self).on_touch_up(touch)

class AndroidBibleApp(App):
    def build(self):
        self.title = "Myanmar and Ethnic Bibles (Created by Ran Aung)"
        self.icon = "app_icon.png"
        
        self.all_bibles_data = {}      
        self.available_versions = []   
        self.ordered_books = []
        self.selected_book = ""
        self.selected_chap = ""
        self.dark_mode = False
        self.book_buttons_refs = []
        self._sync_scrolling = False 
        
        self.selected_verses = {}
        self.verse_item_refs = []
        self.current_testament = "OT" # Default Old Testament
        
        self.highlights_file = os.path.join(self.user_data_dir, 'highlights.json')
        self.notes_file = os.path.join(self.user_data_dir, 'notes.json')
        self.load_userdata()
        
        self.last_scroll_y_1 = 1.0
        self.last_scroll_y_2 = 1.0
        self.toolbar_visible = True
        
        Window.bind(on_keyboard=self.on_key_down)

        self.bibles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bibles")
        if not os.path.exists(self.bibles_dir):
            os.makedirs(self.bibles_dir)

        self.scan_available_versions()

        self.main_layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        with self.main_layout.canvas.before:
            self.root_bg_color = Color(0.95, 0.95, 0.95, 1)
            self.root_bg_rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(pos=self.update_root_rect, size=self.update_root_rect)
        
        # --- Top Action Bar ---
        self.top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=3)
        versions_list = self.available_versions if self.available_versions else ["No Bible"]
        default_version = "BurmeseBible" if "BurmeseBible" in versions_list else versions_list[0]
        
        self.version_spinner_1 = Spinner(text=default_version, values=versions_list, size_hint_x=0.5, font_size='12sp', background_color=[0.2, 0.25, 0.3, 1])
        if os.path.exists(DEFAULT_FONT): self.version_spinner_1.font_name = DEFAULT_FONT
        self.version_spinner_1.bind(text=self.on_version_changed)
        self.top_bar.add_widget(self.version_spinner_1)
        
        self.multi_view_btn = ToggleButton(text="Multi", size_hint_x=None, width='60dp', font_size='12sp', background_color=[0.12, 0.23, 0.35, 1])
        if os.path.exists(DEFAULT_FONT): self.multi_view_btn.font_name = DEFAULT_FONT
        self.multi_view_btn.bind(on_press=self.toggle_multi_view)
        self.top_bar.add_widget(self.multi_view_btn)
        
        self.version_spinner_2 = Spinner(text=default_version, values=versions_list, size_hint_x=0.35, font_size='12sp', background_color=[0.2, 0.25, 0.3, 1])
        if os.path.exists(DEFAULT_FONT): self.version_spinner_2.font_name = DEFAULT_FONT
        self.version_spinner_2.bind(text=self.on_version_changed)
        
        self.theme_btn = Button(text="Dark", size_hint_x=None, width='55dp', font_size='12sp', background_color=[0.12, 0.23, 0.35, 1])
        if os.path.exists(DEFAULT_FONT): self.theme_btn.font_name = DEFAULT_FONT
        self.theme_btn.bind(on_press=self.toggle_app_theme)
        self.top_bar.add_widget(self.theme_btn)
        self.main_layout.add_widget(self.top_bar)
        
        # --- Content Body Layout ---
        self.content_area = BoxLayout(orientation='vertical', spacing=5)
        
        # --- Search Box (Main Page သာ ပြရန်) ---
        self.search_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(42), spacing=5)
        self.search_input = TextInput(hint_text="Search verses...", multiline=False, size_hint_x=0.78, font_size='14sp')
        if os.path.exists(DEFAULT_FONT): self.search_input.font_name = DEFAULT_FONT
        self.search_btn = Button(text="Find", size_hint_x=0.22, font_size='12sp', background_color=[0.15, 0.45, 0.25, 1])
        if os.path.exists(DEFAULT_FONT): self.search_btn.font_name = DEFAULT_FONT
        self.search_btn.bind(on_press=self.execute_bible_search)
        self.search_bar.add_widget(self.search_input)
        self.search_bar.add_widget(self.search_btn)
        
        # --- Navigation Panel ---
        self.nav_panel = BoxLayout(orientation='vertical', spacing=5)
        
        self.nav_top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=5)
        self.btn_my_highlights = Button(text="My Highlights", font_size='12sp', background_color=[0.7, 0.5, 0.2, 1])
        self.btn_my_notes = Button(text="My Notes", font_size='12sp', background_color=[0.2, 0.5, 0.7, 1])
        
        if os.path.exists(DEFAULT_FONT):
            self.btn_my_highlights.font_name = DEFAULT_FONT
            self.btn_my_notes.font_name = DEFAULT_FONT
            
        self.btn_my_highlights.bind(on_press=self.show_highlights_list)
        self.btn_my_notes.bind(on_press=self.show_notes_list)
        self.nav_top_bar.add_widget(self.btn_my_highlights)
        self.nav_top_bar.add_widget(self.btn_my_notes)
        self.nav_panel.add_widget(self.nav_top_bar)
        
        # OT / NT Toggle Bar
        self.testament_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=5)
        self.ot_btn = Button(text="Old Testament (ဟောင်း)", font_size='12sp', background_color=[0.15, 0.35, 0.5, 1])
        self.nt_btn = Button(text="New Testament (သစ်)", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        if os.path.exists(DEFAULT_FONT):
            self.ot_btn.font_name = DEFAULT_FONT
            self.nt_btn.font_name = DEFAULT_FONT
        self.ot_btn.bind(on_press=lambda inst: self.switch_testament("OT"))
        self.nt_btn.bind(on_press=lambda inst: self.switch_testament("NT"))
        self.testament_bar.add_widget(self.ot_btn)
        self.testament_bar.add_widget(self.nt_btn)
        self.nav_panel.add_widget(self.testament_bar)
        
        self.back_btn = Button(text="Back to Books", size_hint_y=None, height=dp(35), disabled=True, font_size='12sp', background_color=[0.12, 0.23, 0.35, 1])
        if os.path.exists(DEFAULT_FONT): self.back_btn.font_name = DEFAULT_FONT
        self.back_btn.bind(on_press=self.go_back_to_books)
        self.nav_panel.add_widget(self.back_btn)
        
        self.grid_scroll = ScrollView()
        self.grid_content = GridLayout(cols=2, spacing=8, size_hint_y=None)
        self.grid_content.bind(minimum_height=self.grid_content.setter('height'))
        self.grid_scroll.add_widget(self.grid_content)
        self.nav_panel.add_widget(self.grid_scroll)
        
        # ပထမအကြိမ်တွင် Search Bar ကိုပါ ထည့်သွင်းပြသမည်
        self.content_area.add_widget(self.search_bar)
        self.content_area.add_widget(self.nav_panel)
        
        # --- Display Text Containers ---
        self.text_views_container = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=0)
        
        self.view1_scroll = SwipeableScrollView(app_ref=self, do_scroll_x=False, do_scroll_y=True)
        self.page_layout_1 = BiblePageLayout()
        self.view1_scroll.add_widget(self.page_layout_1)
        
        self.view2_scroll = SwipeableScrollView(app_ref=self, do_scroll_x=False, do_scroll_y=True)
        self.page_layout_2 = BiblePageLayout()
        self.view2_scroll.add_widget(self.page_layout_2)
        
        self.view1_scroll.bind(scroll_y=self.sync_scroll_v1_to_v2)
        self.view1_scroll.bind(scroll_y=self.track_scroll_y1)
        self.view2_scroll.bind(scroll_y=self.sync_scroll_v2_to_v1)
        self.view2_scroll.bind(scroll_y=self.track_scroll_y2)
        
        self.view1_splitter = Splitter(sizable_from='bottom', size_hint_y=0.5, min_size=80)
        
        # --- Bottom Tool Bars ---
        self.tool_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(42), spacing=5)
        self.hl_btn = Button(text="Highlight", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        self.note_btn = Button(text="Note", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        self.share_btn = Button(text="Share", font_size='12sp', background_color=[0.15, 0.45, 0.25, 1])
        self.close_view_btn = Button(text="Menu", font_size='12sp', background_color=[0.6, 0.2, 0.2, 1])
        
        for btn in [self.hl_btn, self.note_btn, self.share_btn, self.close_view_btn]:
            if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
            
        self.hl_btn.bind(on_press=self.action_highlight)
        self.note_btn.bind(on_press=self.action_add_note)
        self.share_btn.bind(on_press=self.action_share)
        self.close_view_btn.bind(on_press=self.show_navigation_menu)
        
        self.tool_bar.add_widget(self.hl_btn)
        self.tool_bar.add_widget(self.note_btn)
        self.tool_bar.add_widget(self.share_btn)
        self.tool_bar.add_widget(self.close_view_btn)
        
        self.main_layout.add_widget(self.content_area)
        
        if default_version != "No Bible":
            self.load_bible_version(default_version, callback=self.refresh_books_grid)
        else:
            self.refresh_books_grid()
            
        return self.main_layout

    def switch_testament(self, t_type):
        self.current_testament = t_type
        if t_type == "OT":
            self.ot_btn.background_color = [0.15, 0.35, 0.5, 1]
            self.nt_btn.background_color = [0.25, 0.25, 0.25, 1]
        else:
            self.ot_btn.background_color = [0.25, 0.25, 0.25, 1]
            self.nt_btn.background_color = [0.15, 0.35, 0.5, 1]
        self.refresh_books_grid()

    def on_key_down(self, window, key, *args):
        if key in (27, 1001): 
            for child in list(window.children):
                if isinstance(child, Popup):
                    child.dismiss()
                    return True

            if self.text_views_container.size_hint_y == 1:
                self.show_navigation_menu(None)
                return True

            if hasattr(self, 'back_btn') and not self.back_btn.disabled:
                self.go_back_to_books(None)
                return True

            return False
        return False

    def load_userdata(self):
        self.highlights = {}
        self.notes = {}
        if os.path.exists(self.highlights_file):
            try:
                with open(self.highlights_file, 'r', encoding='utf-8') as f:
                    self.highlights = json.load(f)
            except Exception: pass
            
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except Exception: pass

    def save_userdata(self):
        try:
            with open(self.highlights_file, 'w', encoding='utf-8') as f:
                json.dump(self.highlights, f, ensure_ascii=False)
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def show_highlights_list(self, instance):
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        layout.bind(minimum_height=layout.setter('height'))

        if not self.highlights:
            lbl = Label(text="Highlight မှတ်ထားသော ကျမ်းပိုဒ် မရှိသေးပါ။", size_hint_y=None, height=dp(50))
            if os.path.exists(DEFAULT_FONT): lbl.font_name = DEFAULT_FONT
            layout.add_widget(lbl)
        else:
            for key, text_preview in self.highlights.items():
                parts = key.split('_') 
                if len(parts) >= 3:
                    b_name, c_num, v_num = parts[0], parts[1], parts[2]
                    display_b = BURMESE_BOOKS.get(b_name, b_name)
                    
                    btn_text = f"📖 {display_b} {c_num}:{v_num}\n{text_preview[:50]}..."
                    btn = Button(
                        text=btn_text, 
                        size_hint_y=None, 
                        font_size='13sp', 
                        background_color=[0.25, 0.35, 0.45, 1], 
                        halign='left', 
                        valign='middle',
                        padding=(dp(10), dp(10))
                    )
                    # Dynamic Height Binding
                    btn.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(20), None)))
                    btn.bind(texture_size=lambda s, ts: setattr(s, 'height', ts[1] + dp(20)))
                    
                    if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
                    btn.bind(on_press=lambda inst, b=b_name, c=c_num, v=v_num: self.go_to_search_target(b, c, v, popup))
                    layout.add_widget(btn)

        scroll.add_widget(layout)
        popup = Popup(title="My Highlights", content=scroll, size_hint=(0.95, 0.8))
        popup.open()

    def show_notes_list(self, instance):
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        layout.bind(minimum_height=layout.setter('height'))

        if not self.notes:
            lbl = Label(text="ရေးသားထားသော မှတ်စု မရှိသေးပါ။", size_hint_y=None, height=dp(50))
            if os.path.exists(DEFAULT_FONT): lbl.font_name = DEFAULT_FONT
            layout.add_widget(lbl)
        else:
            for key, note_data in self.notes.items():
                parts = key.split('_')
                if len(parts) >= 3:
                    b_name, c_num = parts[0], parts[1]
                    display_b = BURMESE_BOOKS.get(b_name, b_name)
                    verses = note_data.get('verses', '')
                    note_text = note_data.get('note', '')
                    
                    btn_text = f"📝 {display_b} {c_num}:{verses}\n{note_text[:50]}..."
                    btn = Button(
                        text=btn_text, 
                        size_hint_y=None, 
                        font_size='13sp', 
                        background_color=[0.2, 0.4, 0.3, 1], 
                        halign='left', 
                        valign='middle',
                        padding=(dp(10), dp(10))
                    )
                    # Dynamic Height Binding
                    btn.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(20), None)))
                    btn.bind(texture_size=lambda s, ts: setattr(s, 'height', ts[1] + dp(20)))
                    
                    if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
                    btn.bind(on_press=lambda inst, b=b_name, c=c_num, v=verses: self.go_to_search_target(b, c, v, popup))
                    layout.add_widget(btn)

        scroll.add_widget(layout)
        popup = Popup(title="My Notes", content=scroll, size_hint=(0.95, 0.8))
        popup.open()

    def add_selected_verse(self, v_num, v_text):
        self.selected_verses[v_num] = v_text
        
    def remove_selected_verse(self, v_num):
        if v_num in self.selected_verses:
            del self.selected_verses[v_num]
            
    def clear_selections(self):
        self.selected_verses.clear()
        for v_item in self.verse_item_refs:
            if v_item.is_selected:
                v_item.is_selected = False
                v_item.update_bg_color() 

    def show_popup_msg(self, msg):
        lbl = Label(text=msg, font_name=DEFAULT_FONT if os.path.exists(DEFAULT_FONT) else None)
        popup = Popup(title='Message', content=lbl, size_hint=(0.8, 0.3))
        popup.open()

    def action_highlight(self, instance):
        if not self.selected_verses:
            self.show_popup_msg("ကျေးဇူးပြု၍ ကျမ်းပိုဒ်ကို အရင်ရွေးချယ်ပါ။")
            return
            
        for v_num, v_text in self.selected_verses.items():
            key = f"{self.selected_book}_{self.selected_chap}_{v_num}"
            if key in self.highlights:
                del self.highlights[key] 
            else:
                self.highlights[key] = v_text
                
        self.save_userdata()
        
        for v_item in self.verse_item_refs:
            key = f"{self.selected_book}_{self.selected_chap}_{v_item.verse_num}"
            v_item.is_highlighted = (key in self.highlights)
            
        self.clear_selections()
        self.show_popup_msg("Highlight မှတ်သား/ဖြုတ်သိမ်းခြင်း ပြီးပါပြီ။")

    def action_add_note(self, instance):
        if not self.selected_verses:
            self.show_popup_msg("ကျေးဇူးပြု၍ ကျမ်းပိုဒ်ကို အရင်ရွေးချယ်ပါ။")
            return
            
        v_nums = ", ".join(sorted(self.selected_verses.keys(), key=lambda x: int(x) if x.isdigit() else 0))
        first_v = sorted(self.selected_verses.keys(), key=lambda x: int(x) if x.isdigit() else 0)[0]
        key = f"{self.selected_book}_{self.selected_chap}_{first_v}"
        
        existing_note = self.notes.get(key, {}).get('note', "")
        
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        note_input = TextInput(text=existing_note, hint_text=f"ကျမ်းပိုဒ် {v_nums} အတွက် မှတ်စုရေးရန်...", multiline=True)
        if os.path.exists(DEFAULT_FONT): note_input.font_name = DEFAULT_FONT
        
        save_btn = Button(text="Save Note", size_hint_y=None, height=dp(45), background_color=[0.12, 0.23, 0.35, 1])
        if os.path.exists(DEFAULT_FONT): save_btn.font_name = DEFAULT_FONT
        
        box.add_widget(note_input)
        box.add_widget(save_btn)
        popup = Popup(title='Add Note', content=box, size_hint=(0.9, 0.5))
        
        def on_save_btn_pressed(btn):
            note_text = note_input.text.strip()
            if note_text:
                self.notes[key] = {
                    'verses': v_nums,
                    'note': note_text
                }
            else:
                if key in self.notes:
                    del self.notes[key]
                    
            self.save_userdata()
            popup.dismiss()
            self.clear_selections()
            self.show_popup_msg("မှတ်စု သိမ်းဆည်းပြီးပါပြီ။")

        save_btn.bind(on_press=on_save_btn_pressed)
        popup.open()

    def action_share(self, instance):
        if not self.selected_verses:
            self.show_popup_msg("ကျေးဇူးပြု၍ ကျမ်းပိုဒ်ကို အရင်ရွေးချယ်ပါ။")
            return
            
        b_name = BURMESE_BOOKS.get(self.selected_book, self.selected_book)
        shared_text = f"📖 {b_name} {self.selected_chap}\n\n"
        
        sorted_keys = sorted(self.selected_verses.keys(), key=lambda x: int(x) if x.isdigit() else 0)
        for k in sorted_keys:
            shared_text += f"{k}. {self.selected_verses[k]}\n"
            
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                String = autoclass('java.lang.String')
                
                intent = Intent()
                intent.setAction(Intent.ACTION_SEND)
                intent.putExtra(Intent.EXTRA_TEXT, String(shared_text))
                intent.setType("text/plain")
                
                chooser = Intent.createChooser(intent, String("Share Bible Verses"))
                PythonActivity.mActivity.startActivity(chooser)
            except Exception as e:
                self.show_popup_msg("Share လုပ်ရာတွင် အခက်အခဲရှိနေပါသည်။")
        else:
            box = BoxLayout(orientation='vertical', padding=10, spacing=10)
            txt = TextInput(text=shared_text, multiline=True, readonly=True)
            if os.path.exists(DEFAULT_FONT): txt.font_name = DEFAULT_FONT
            box.add_widget(txt)
            popup = Popup(title='Shared Content', content=box, size_hint=(0.9, 0.6))
            popup.open()
            
        self.clear_selections()

    def navigate_chapter(self, direction):
        if not self.selected_book or not self.selected_chap:
            return
        active_ver = self.version_spinner_1.text
        if active_ver not in self.all_bibles_data: return
        book_data = self.all_bibles_data[active_ver]
        if self.selected_book not in book_data: return
        books_list = list(book_data.keys())
        try: book_idx = books_list.index(self.selected_book)
        except ValueError: return
        
        chapters_list = sorted(list(book_data[self.selected_book].keys()), key=lambda x: int(x) if x.isdigit() else 0)
        try: chap_idx = chapters_list.index(self.selected_chap)
        except ValueError: return
            
        changed = False
        if direction == "next":
            if chap_idx + 1 < len(chapters_list):
                self.selected_chap = chapters_list[chap_idx + 1]
                changed = True
            else:
                if book_idx + 1 < len(books_list):
                    self.selected_book = books_list[book_idx + 1]
                    new_chaps = sorted(list(book_data[self.selected_book].keys()), key=lambda x: int(x) if x.isdigit() else 0)
                    if new_chaps:
                        self.selected_chap = new_chaps[0]
                        changed = True
        elif direction == "prev":
            if chap_idx - 1 >= 0:
                self.selected_chap = chapters_list[chap_idx - 1]
                changed = True
            else:
                if book_idx - 1 >= 0:
                    self.selected_book = books_list[book_idx - 1]
                    new_chaps = sorted(list(book_data[self.selected_book].keys()), key=lambda x: int(x) if x.isdigit() else 0)
                    if new_chaps:
                        self.selected_chap = new_chaps[-1]
                        changed = True
                        
        if changed:
            self.show_bible_text_view()

    def track_scroll_y1(self, instance, value):
        self.check_scroll_direction(value, 1)

    def track_scroll_y2(self, instance, value):
        self.check_scroll_direction(value, 2)

    def check_scroll_direction(self, current_y, view_num):
        last_y_attr = f'last_scroll_y_{view_num}'
        last_y = getattr(self, last_y_attr, 1.0)
        
        diff = current_y - last_y
        if abs(diff) < 0.03 and 0.02 < current_y < 0.98:
            return  

        if current_y >= 0.98:
            if not self.toolbar_visible: self.show_toolbar()
            setattr(self, last_y_attr, current_y)
            return

        if diff < -0.03:
            if self.toolbar_visible: self.hide_toolbar()
            setattr(self, last_y_attr, current_y)
        elif diff > 0.03:
            if not self.toolbar_visible: self.show_toolbar()
            setattr(self, last_y_attr, current_y)

    def hide_toolbar(self):
        if self.toolbar_visible:
            self.tool_bar.height = 0
            self.tool_bar.opacity = 0
            self.tool_bar.disabled = True
            self.toolbar_visible = False

    def show_toolbar(self):
        if not self.toolbar_visible:
            self.tool_bar.height = dp(42)
            self.tool_bar.opacity = 1
            self.tool_bar.disabled = False
            self.toolbar_visible = True

    def update_root_rect(self, instance, value):
        self.root_bg_rect.pos = instance.pos
        self.root_bg_rect.size = instance.size

    def sync_scroll_v1_to_v2(self, instance, value):
        if not self._sync_scrolling and self.multi_view_btn.state == 'down':
            self._sync_scrolling = True
            self.view2_scroll.scroll_y = value
            self._sync_scrolling = False

    def sync_scroll_v2_to_v1(self, instance, value):
        if not self._sync_scrolling and self.multi_view_btn.state == 'down':
            self._sync_scrolling = True
            self.view1_scroll.scroll_y = value
            self._sync_scrolling = False

    def scan_available_versions(self):
        self.available_versions = []
        if not os.path.exists(self.bibles_dir): return
        try: files = [f for f in os.listdir(self.bibles_dir) if f.endswith('.xml')]
        except Exception: return
        
        for file in files:
            version_name = os.path.splitext(file)[0]
            if version_name not in self.available_versions:
                self.available_versions.append(version_name)

        if not self.available_versions:
            self.available_versions = ["No Bible"]

    def load_bible_version(self, version_name, callback=None):
        if version_name in self.all_bibles_data or version_name == "No Bible":
            if callback: callback()
            return
            
        if getattr(self, 'is_loading_xml', False):
            Clock.schedule_once(lambda dt: self.load_bible_version(version_name, callback), 0.5)
            return
            
        self.is_loading_xml = True
        
        self.loading_popup = Popup(
            title="Loading Bible", 
            content=Label(text=f"Parsing {version_name}...\nPlease wait."), 
            size_hint=(0.8, 0.3), 
            auto_dismiss=False
        )
        if os.path.exists(DEFAULT_FONT):
            self.loading_popup.content.font_name = DEFAULT_FONT
        self.loading_popup.open()
        
        def parse_xml_thread():
            xml_path = os.path.join(self.bibles_dir, f"{version_name}.xml")
            if not os.path.exists(xml_path):
                Clock.schedule_once(lambda dt: self._finish_loading(callback), 0)
                return
                
            try:
                with open(xml_path, 'r', encoding='utf-8-sig') as f:
                    xml_content = f.read()
                root_element = ET.fromstring(xml_content)
                
                bible_data = {}
                temp_ordered_books = []
                
                all_books = root_element.findall('.//book') + root_element.findall('.//Book') + root_element.findall('.//b')
                for idx, book in enumerate(all_books):
                    book_name_attr = book.get('name') or book.get('n') or book.get('number') or book.get('id') or book.get('bcode')
                    if book_name_attr and book_name_attr in BIBLE_BOOKS:
                        book_name = BIBLE_BOOKS[book_name_attr]
                    elif not book_name_attr:
                        book_name = BIBLE_BOOKS.get(str(idx + 1), str(idx + 1))
                    else:
                        book_name = str(book_name_attr).strip()
                    
                    if book_name not in bible_data:
                        bible_data[book_name] = {}
                        if book_name not in temp_ordered_books:
                            temp_ordered_books.append(book_name)
                    
                    all_chapters = book.findall('.//chapter') + book.findall('.//Chapter') + book.findall('.//c')
                    for c_idx, chapter in enumerate(all_chapters):
                        ch_num = chapter.get('number') or chapter.get('n') or chapter.get('id') or str(c_idx + 1)
                        ch_num_str = str(ch_num).strip()
                        bible_data[book_name][ch_num_str] = {}
                        
                        all_verses = chapter.findall('.//verse') + chapter.findall('.//Verse') + chapter.findall('.//v')
                        for v_idx, verse in enumerate(all_verses):
                            v_num = verse.get('number') or verse.get('n') or verse.get('id') or str(v_idx + 1)
                            v_num_str = str(v_num).strip()
                            
                            v_text = "".join(verse.itertext()) if verse is not None else ""
                            v_text = " ".join(v_text.split()) 
                            
                            bible_data[book_name][ch_num_str][v_num_str] = v_text
                
                Clock.schedule_once(lambda dt: self._apply_parsed_data(version_name, bible_data, temp_ordered_books, callback), 0)
            except Exception as e:
                print(f"Error parsing {version_name}: {e}")
                Clock.schedule_once(lambda dt: self._finish_loading(callback), 0)
                
        threading.Thread(target=parse_xml_thread, daemon=True).start()
        
    def _apply_parsed_data(self, version_name, bible_data, temp_ordered_books, callback):
        self.all_bibles_data[version_name] = bible_data
        if temp_ordered_books and not self.ordered_books:
            self.ordered_books = temp_ordered_books
        self._finish_loading(callback)
        
    def _finish_loading(self, callback):
        self.is_loading_xml = False
        if hasattr(self, 'loading_popup') and self.loading_popup:
            self.loading_popup.dismiss()
        if callback:
            callback()

    def refresh_books_grid(self, *args):
        active_ver = self.version_spinner_1.text
        
        def _render_books():
            self.grid_content.clear_widgets()
            self.book_buttons_refs.clear()
            self.grid_content.cols = 2
            self.back_btn.disabled = True
            
            target_list = OT_BOOKS if self.current_testament == "OT" else NT_BOOKS
            available_books = [b for b in target_list if b in self.ordered_books]
            if not available_books and self.ordered_books:
                # Fallback if names differ slightly
                mid = len(self.ordered_books) // 2
                available_books = self.ordered_books[:mid] if self.current_testament == "OT" else self.ordered_books[mid:]

            for book_name in available_books:
                bg_color = [0.2, 0.2, 0.2, 1] if self.dark_mode else [0.85, 0.85, 0.85, 1]
                text_color = [1, 1, 1, 1] 
                display_name = BURMESE_BOOKS.get(book_name, book_name) if active_ver == "BurmeseBible" else book_name
                
                btn = Button(text=display_name, size_hint_y=None, height=dp(48), font_size='13sp', background_color=bg_color, color=text_color)
                if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
                btn.bind(on_press=lambda instance, b=book_name: self.on_book_selected(b))
                self.grid_content.add_widget(btn)
                self.book_buttons_refs.append(btn)
                
        if active_ver not in self.all_bibles_data:
            self.load_bible_version(active_ver, callback=_render_books)
        else:
            _render_books()

    def on_book_selected(self, book_name):
        self.selected_book = book_name
        self.grid_content.clear_widgets()
        self.book_buttons_refs.clear()
        self.grid_content.cols = 4
        self.back_btn.disabled = False
        
        # Book ရွေးလိုက်ပြီဖြစ်၍ OT/NT Bar နဲ့ Search Bar ကို ဖျောက်မည်
        if self.testament_bar.parent:
            self.nav_panel.remove_widget(self.testament_bar)
        if self.search_bar.parent:
            self.content_area.remove_widget(self.search_bar)
        
        active_ver = self.version_spinner_1.text
        
        def _render_chapters():
            if active_ver in self.all_bibles_data and self.selected_book in self.all_bibles_data[active_ver]:
                chapters = sorted(list(self.all_bibles_data[active_ver][self.selected_book].keys()), key=lambda x: int(x) if x.isdigit() else 0)
                for ch_num in chapters:
                    bg_color = [0.25, 0.25, 0.25, 1] if self.dark_mode else [0.8, 0.8, 0.8, 1]
                    btn = Button(text=str(ch_num), size_hint_y=None, height=dp(48), font_size='14sp', background_color=bg_color, color=[1, 1, 1, 1])
                    if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
                    btn.bind(on_press=lambda instance, c=ch_num: self.on_chapter_selected(c))
                    self.grid_content.add_widget(btn)
                    self.book_buttons_refs.append(btn)
                    
        if active_ver not in self.all_bibles_data:
            self.load_bible_version(active_ver, callback=_render_chapters)
        else:
            _render_chapters()

    def on_chapter_selected(self, ch_num):
        self.selected_chap = ch_num
        Clock.schedule_once(lambda dt: self.show_bible_text_view(), 0)

    def go_to_search_target(self, book, chapter, verse_num, popup_to_close):
        if popup_to_close:
            popup_to_close.dismiss()
        self.selected_book = book
        self.selected_chap = chapter
        self.show_bible_text_view()

    def go_back_to_books(self, instance):
        # Book list ပြန်လာချိန်တွင် Search Bar နှင့် OT/NT Bar ကို ပြန်ထည့်မည်
        if self.search_bar.parent not in self.content_area.children:
            self.content_area.remove_widget(self.nav_panel)
            self.content_area.add_widget(self.search_bar)
            self.content_area.add_widget(self.nav_panel)
        if self.testament_bar.parent not in self.nav_panel.children:
            self.nav_panel.remove_widget(self.back_btn)
            self.nav_panel.remove_widget(self.grid_scroll)
            self.nav_panel.add_widget(self.testament_bar)
            self.nav_panel.add_widget(self.back_btn)
            self.nav_panel.add_widget(self.grid_scroll)
        self.refresh_books_grid()

    def show_bible_text_view(self):
        # Text view ရောက်လျှင် Search bar နှင့် OT/NT bar ကို လုံးဝဖျောက်ထားမည်
        if self.search_bar.parent:
            self.content_area.remove_widget(self.search_bar)
        if self.testament_bar.parent:
            self.nav_panel.remove_widget(self.testament_bar)
            
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.text_views_container)
        self.content_area.add_widget(self.tool_bar) 
        self.show_toolbar() 
        self.text_views_container.size_hint_y = 1
        
        self.update_text_views_layout()
        self.display_bible_verses()

    def show_navigation_menu(self, instance):
        if self.view1_scroll.parent: self.view1_scroll.parent.remove_widget(self.view1_scroll)
        if self.view2_scroll.parent: self.view2_scroll.parent.remove_widget(self.view2_scroll)
        if self.view1_splitter.parent: self.view1_splitter.parent.remove_widget(self.view1_splitter)
            
        self.text_views_container.clear_widgets()
        self.content_area.clear_widgets()
        
        # Menu ပြန်လာလျှင် Search Bar ပြန်ထည့်မည် (OT/NT bar မပါတော့ဘဲ Chapter list သို့မဟုတ် Book list ပြရန်)
        if self.search_bar.parent not in self.content_area.children:
            self.content_area.add_widget(self.search_bar)
        self.content_area.add_widget(self.nav_panel)
        self.text_views_container.size_hint_y = None
        self.text_views_container.height = 0
        self.on_book_selected(self.selected_book)

    def toggle_multi_view(self, instance):
        def _finish_toggle():
            self.update_text_views_layout()
            self.display_bible_verses()
            
        if instance.state == 'down':
            if self.version_spinner_2 not in self.top_bar.children:
                self.top_bar.add_widget(self.version_spinner_2)
                ver2 = self.version_spinner_2.text
                if ver2 not in self.all_bibles_data:
                    self.load_bible_version(ver2, callback=_finish_toggle)
                else:
                    _finish_toggle()
        else:
            if self.version_spinner_2 in self.top_bar.children:
                self.top_bar.remove_widget(self.version_spinner_2)
            _finish_toggle()

    def update_text_views_layout(self):
        if self.view1_scroll.parent: self.view1_scroll.parent.remove_widget(self.view1_scroll)
        if self.view2_scroll.parent: self.view2_scroll.parent.remove_widget(self.view2_scroll)
        if self.view1_splitter.parent: self.view1_splitter.parent.remove_widget(self.view1_splitter)
            
        self.text_views_container.clear_widgets()
        if self.multi_view_btn.state == 'down':
            self.view1_splitter.add_widget(self.view1_scroll)
            self.text_views_container.add_widget(self.view1_splitter)
            self.text_views_container.add_widget(self.view2_scroll)
        else:
            self.text_views_container.add_widget(self.view1_scroll)

    def on_version_changed(self, spinner, text):
        def _after_version_changed():
            if self.back_btn.disabled: self.refresh_books_grid()
            else: self.on_book_selected(self.selected_book)
            
            if self.text_views_container.size_hint_y == 1:
                self.display_bible_verses()
                
        if text not in self.all_bibles_data:
            self.load_bible_version(text, callback=_after_version_changed)
        else:
            _after_version_changed()

    def populate_page(self, page_layout, version_name):
        page_layout.clear_widgets()
        page_layout.current_load_id = time.time()  
        
        if not version_name or version_name not in self.all_bibles_data: return

        selected_font = get_font_for_version(version_name)
        display_book = BURMESE_BOOKS.get(self.selected_book, self.selected_book) if version_name == "BurmeseBible" else self.selected_book

        header_lbl = Label(
            text=f"=== {display_book} (Chapter {self.selected_chap}) [{version_name}] ===",
            font_name=selected_font if selected_font else DEFAULT_FONT,
            color=[0.2, 0.4, 0.8, 1] if not self.dark_mode else [1, 0.8, 0.2, 1],
            size_hint_y=None, height=dp(50), bold=True,
            halign='center', valign='middle'
        )
        header_lbl.bind(size=lambda s, w: setattr(s, 'text_size', s.size))
        page_layout.add_widget(header_lbl)

        book_data = self.all_bibles_data[version_name].get(self.selected_book, {})
        chapter_data = book_data.get(self.selected_chap, {})
        
        if chapter_data:
            sorted_verses = sorted(list(chapter_data.keys()), key=lambda x: int(x) if x.isdigit() else 0)
            self._load_verses_chunk(page_layout, sorted_verses, chapter_data, selected_font, version_name, page_layout.current_load_id, 0)

    def _load_verses_chunk(self, page_layout, sorted_verses, chapter_data, selected_font, version_name, load_id, current_idx):
        if not hasattr(page_layout, 'current_load_id') or page_layout.current_load_id != load_id:
            return  
            
        chunk_size = 15  
        end_idx = min(current_idx + chunk_size, len(sorted_verses))
        
        for i in range(current_idx, end_idx):
            v_key = sorted_verses[i]
            v_text = chapter_data[v_key]
            global_key = f"{self.selected_book}_{self.selected_chap}_{v_key}"
            is_hl = (global_key in self.highlights)
            
            v_item = VerseItem(
                verse_num=v_key, 
                verse_text=v_text, 
                app_ref=self, 
                is_dark_mode=self.dark_mode,
                font_name=selected_font,
                is_highlighted=is_hl
            )
            page_layout.add_widget(v_item)
            if v_item not in self.verse_item_refs:
                self.verse_item_refs.append(v_item)
                
        if end_idx < len(sorted_verses):
            Clock.schedule_once(lambda dt: self._load_verses_chunk(page_layout, sorted_verses, chapter_data, selected_font, version_name, load_id, end_idx), 0)

    def display_bible_verses(self):
        if not self.selected_book or not self.selected_chap:
            return
            
        def _render_verses():
            self.clear_selections()
            self.verse_item_refs.clear()
            self.populate_page(self.page_layout_1, self.version_spinner_1.text)
            
            if self.multi_view_btn.state == 'down':
                def _render_view2():
                    self.populate_page(self.page_layout_2, self.version_spinner_2.text)
                    self.view1_scroll.scroll_y = 1.0
                    self.view2_scroll.scroll_y = 1.0
                    
                ver2 = self.version_spinner_2.text
                if ver2 not in self.all_bibles_data:
                    self.load_bible_version(ver2, callback=_render_view2)
                else:
                    _render_view2()
            else:
                self.view1_scroll.scroll_y = 1.0
                self.view2_scroll.scroll_y = 1.0
                
        ver1 = self.version_spinner_1.text
        if ver1 not in self.all_bibles_data:
            self.load_bible_version(ver1, callback=_render_verses)
        else:
            _render_verses()

    def execute_bible_search(self, instance):
        # ရှာဖွေရာတွင် မြန်မာစာ Zero-width space ပြဿနာမရှိစေရန် ရှင်းလင်းခြင်း
        query = self.search_input.text.strip().replace('\u200b', '')
        query_lower = query.lower()
        active_ver = self.version_spinner_1.text
        if not query: return
        
        def _do_search():
            if active_ver not in self.all_bibles_data: return
            
            results = []
            for b_name, chapters in self.all_bibles_data[active_ver].items():
                for ch_num, verses in chapters.items():
                    for v_num, v_text in verses.items():
                        clean_v_text = v_text.replace('\u200b', '')
                        # တိုက်စစ်ရာတွင် ပိုမိုတိကျစေရန်
                        if query in clean_v_text or query_lower in clean_v_text.lower():
                            results.append((b_name, ch_num, v_num, clean_v_text))

            is_limited = False
            if len(results) > 100:
                results = results[:100]
                is_limited = True
                
            scroll = ScrollView()
            results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
            results_layout.bind(minimum_height=results_layout.setter('height'))
            
            if not results:
                lbl = Label(text=f"No results found for '{query}'", size_hint_y=None, height=dp(40))
                if os.path.exists(DEFAULT_FONT): lbl.font_name = DEFAULT_FONT
                results_layout.add_widget(lbl)
            else:
                if is_limited:
                    lbl = Label(text=f"Showing top 100 results for '{query}'", size_hint_y=None, height=dp(30), color=[1, 0.5, 0, 1])
                    if os.path.exists(DEFAULT_FONT): lbl.font_name = DEFAULT_FONT
                    results_layout.add_widget(lbl)
                    
                for r in results:
                    b_display = BURMESE_BOOKS.get(r[0], r[0]) if active_ver == "BurmeseBible" else r[0]
                    btn_text = f"[b]{b_display} {r[1]}:{r[2]}[/b]\n{r[3]}"
                    
                    btn = Button(
                        text=btn_text, 
                        markup=True,
                        size_hint_y=None, 
                        font_size='14sp', 
                        background_color=[0.25, 0.35, 0.45, 1],
                        halign='left',
                        valign='middle',
                        padding=(dp(10), dp(10)) # စာသားနှင့်ဘောင် မထိစေရန်
                    )
                    
                    # Button အမြင့်ကို စာသားအရှည်ပေါ်မူတည်ပြီး Dynamic အပြောင်းအလဲလုပ်ပေးခြင်း
                    btn.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(20), None)))
                    btn.bind(texture_size=lambda s, ts: setattr(s, 'height', ts[1] + dp(20)))
                    
                    if os.path.exists(DEFAULT_FONT): btn.font_name = DEFAULT_FONT
                    
                    btn.bind(on_press=lambda inst, b=r[0], c=r[1], v=r[2]: self.go_to_search_target(b, c, v, popup))
                    results_layout.add_widget(btn)
                    
            scroll.add_widget(results_layout)
            popup = Popup(title=f"Search Results ({len(results)})", content=scroll, size_hint=(0.95, 0.8))
            popup.open()
            
        if active_ver not in self.all_bibles_data:
            self.load_bible_version(active_ver, callback=_do_search)
        else:
            _do_search()

    def toggle_app_theme(self, instance):
        self.dark_mode = not self.dark_mode
        self.theme_btn.text = "Light" if self.dark_mode else "Dark"
        self.root_bg_color.rgba = [0.1, 0.12, 0.15, 1] if self.dark_mode else [0.95, 0.95, 0.95, 1]
            
        for btn in self.book_buttons_refs:
            if self.dark_mode:
                btn.background_color = [0.2, 0.2, 0.2, 1] if self.grid_content.cols == 2 else [0.25, 0.25, 0.25, 1]
            else:
                btn.background_color = [0.85, 0.85, 0.85, 1] if self.grid_content.cols == 2 else [0.8, 0.8, 0.8, 1]

        for v_item in self.verse_item_refs:
            v_item.apply_theme_colors(self.dark_mode)

if __name__ == "__main__":
    AndroidBibleApp().run()