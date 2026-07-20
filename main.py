import os
import xml.etree.ElementTree as ET
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
from kivy.utils import platform
from kivy.graphics import Color, Rectangle

# Myanmar Font လမ်းကြောင်း စစ်ဆေးခြင်း
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MyanmarSage.ttf")
if not os.path.exists(FONT_PATH):
    FONT_PATH = None  

# Bible book names database mappings (English)
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

# 💡 မြန်မာကျမ်းစာစောင်အမည်များအတွက် Mapping Dictionary
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
    "2 Peter": "ပေတရုဒုテイယစောင်", "1 John": "ယောဟန်ပထမစောင်", "2 John": "ယောဟန်ဒုတိယစောင်", "3 John": "ယောဟန်တတိယစောင်", "Jude": "ယုဒစာ",
    "Revelation": "ဗျာဒိတ်ကျမ်း"
}

class ScrollableBibleLabel(Label):
    def __init__(self, **kwargs):
        super(ScrollableBibleLabel, self).__init__(**kwargs)
        self.size_hint_y = None
        self.halign = 'center' 
        self.valign = 'top'
        self.padding = (15, 15)
        self.color = [0, 0, 0, 1]
        if FONT_PATH:
            self.font_name = FONT_PATH
        
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(size=self.update_text_width)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_text_width(self, *args):
        self.text_size = (self.width - self.padding[0]*2, None)

    def on_texture_size(self, *args):
        self.height = max(self.texture_size[1] + self.padding[1]*2, 200)


class AndroidBibleApp(App):
    def build(self):
        self.title = "Myanmar and Ethnic Bibles (Created by Ran Aung)"
        self.icon = "app_icon.png"  # 💡 APK အတွင်းပိုင်း Logo Icon သတ်မှတ်ခြင်း
        
        self.all_bibles_data = {}
        self.ordered_books = []
        self.selected_book = ""
        self.selected_chap = ""
        self.dark_mode = False
        self.book_buttons_refs = []
        self._sync_scrolling = False 
        self.bibles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bibles")
            
        if not os.path.exists(self.bibles_dir):
            os.makedirs(self.bibles_dir)

        self.load_all_available_bibles()

        self.main_layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        with self.main_layout.canvas.before:
            self.root_bg_color = Color(0.95, 0.95, 0.95, 1)
            self.root_bg_rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(pos=self.update_root_rect, size=self.update_root_rect)
        
        # --- Top Action Bar ---
        self.top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height='45dp', spacing=3)
        
        versions_list = list(self.all_bibles_data.keys()) if self.all_bibles_data else ["No Bible"]
        
        default_version = "BurmeseBible" if "BurmeseBible" in versions_list else versions_list[0]
        
        self.version_spinner_1 = Spinner(text=default_version, values=versions_list, size_hint_x=0.5, font_size='12sp', background_color=[0.2, 0.25, 0.3, 1])
        if FONT_PATH: self.version_spinner_1.font_name = FONT_PATH
        self.version_spinner_1.bind(text=self.on_version_changed)
        self.top_bar.add_widget(self.version_spinner_1)
        
        self.multi_view_btn = ToggleButton(text="Multi", size_hint_x=None, width='60dp', font_size='12sp', background_color=[0.12, 0.23, 0.35, 1])
        if FONT_PATH: self.multi_view_btn.font_name = FONT_PATH
        self.multi_view_btn.bind(on_press=self.toggle_multi_view)
        self.top_bar.add_widget(self.multi_view_btn)
        
        self.version_spinner_2 = Spinner(text=default_version, values=versions_list, size_hint_x=0.35, font_size='12sp', background_color=[0.2, 0.25, 0.3, 1])
        if FONT_PATH: self.version_spinner_2.font_name = FONT_PATH
        self.version_spinner_2.bind(text=self.on_version_changed)
        
        self.theme_btn = Button(text="Dark", size_hint_x=None, width='55dp', font_size='12sp', background_color=[0.12, 0.23, 0.35, 1])
        if FONT_PATH: self.theme_btn.font_name = FONT_PATH
        self.theme_btn.bind(on_press=self.toggle_app_theme)
        self.top_bar.add_widget(self.theme_btn)
        
        self.main_layout.add_widget(self.top_bar)
        
        # --- Search Box ---
        self.search_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height='42dp', spacing=5)
        self.search_input = TextInput(hint_text="Search verses...", multiline=False, size_hint_x=0.78, font_size='14sp')
        if FONT_PATH: self.search_input.font_name = FONT_PATH
        
        self.search_btn = Button(text="Find", size_hint_x=0.22, font_size='12sp', background_color=[0.15, 0.45, 0.25, 1])
        if FONT_PATH: self.search_btn.font_name = FONT_PATH
        self.search_btn.bind(on_press=self.execute_bible_search)
        self.search_bar.add_widget(self.search_input)
        self.search_bar.add_widget(self.search_btn)
        self.main_layout.add_widget(self.search_bar)
        
        # --- Content Body Layout ---
        self.content_area = BoxLayout(orientation='vertical', spacing=5)
        
        self.nav_panel = BoxLayout(orientation='vertical', spacing=5)
        
        self.back_btn = Button(text="Back to Books", size_hint_y=None, height='42dp', disabled=True, font_size='13sp', background_color=[0.12, 0.23, 0.35, 1])
        if FONT_PATH: self.back_btn.font_name = FONT_PATH
        self.back_btn.bind(on_press=self.go_back_to_books)
        self.nav_panel.add_widget(self.back_btn)
        
        self.grid_scroll = ScrollView()
        self.grid_content = GridLayout(cols=2, spacing=8, size_hint_y=None)
        self.grid_content.bind(minimum_height=self.grid_content.setter('height'))
        self.grid_scroll.add_widget(self.grid_content)
        self.nav_panel.add_widget(self.grid_scroll)
        
        self.content_area.add_widget(self.nav_panel)
        
        # --- Display Text Containers ---
        self.text_views_container = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=0)
        
        self.view1_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.text_display_1 = ScrollableBibleLabel(font_size='16sp')
        self.view1_scroll.add_widget(self.text_display_1)
        
        self.view2_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.text_display_2 = ScrollableBibleLabel(font_size='16sp')
        self.view2_scroll.add_widget(self.text_display_2)
        
        self.view1_scroll.bind(scroll_y=self.sync_scroll_v1_to_v2)
        self.view2_scroll.bind(scroll_y=self.sync_scroll_v2_to_v1)
        
        self.view1_splitter = Splitter(sizable_from='bottom', size_hint_y=0.5, min_size=80)
        
        # Bottom Tool Bars
        self.tool_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height='42dp', spacing=5)
        self.hl_btn = Button(text="Highlight", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        self.note_btn = Button(text="Note", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        self.close_view_btn = Button(text="Menu", font_size='12sp', background_color=[0.25, 0.25, 0.25, 1])
        
        if FONT_PATH:
            self.hl_btn.font_name = FONT_PATH
            self.note_btn.font_name = FONT_PATH
            self.close_view_btn.font_name = FONT_PATH
            
        self.hl_btn.bind(on_press=self.action_highlight)
        self.note_btn.bind(on_press=self.action_add_note)
        self.close_view_btn.bind(on_press=self.show_navigation_menu)
        
        self.tool_bar.add_widget(self.hl_btn)
        self.tool_bar.add_widget(self.note_btn)
        self.tool_bar.add_widget(self.close_view_btn)
        
        self.main_layout.add_widget(self.content_area)
        
        self.refresh_books_grid()
        return self.main_layout

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

    def load_all_available_bibles(self):
        self.all_bibles_data.clear()
        if not os.path.exists(self.bibles_dir):
            return
        try:
            files = [f for f in os.listdir(self.bibles_dir) if f.endswith('.xml')]
        except:
            return
        
        for file in files:
            version_name = os.path.splitext(file)[0]
            xml_path = os.path.join(self.bibles_dir, file)
            try:
                tree = ET.parse(xml_path)
                root_element = tree.getroot()
                self.all_bibles_data[version_name] = {}
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
                    
                    if book_name not in self.all_bibles_data[version_name]:
                        self.all_bibles_data[version_name][book_name] = {}
                        if book_name not in temp_ordered_books:
                            temp_ordered_books.append(book_name)
                    
                    all_chapters = book.findall('.//chapter') + book.findall('.//Chapter') + book.findall('.//c')
                    for c_idx, chapter in enumerate(all_chapters):
                        ch_num = chapter.get('number') or chapter.get('n') or chapter.get('id')
                        if not ch_num:
                            ch_num = str(c_idx + 1)
                            
                        ch_num_str = str(ch_num).strip()
                        self.all_bibles_data[version_name][book_name][ch_num_str] = {}
                        
                        all_verses = chapter.findall('.//verse') + chapter.findall('.//Verse') + chapter.findall('.//v')
                        for v_idx, verse in enumerate(all_verses):
                            v_num = verse.get('number') or verse.get('n') or verse.get('id')
                            if not v_num:
                                v_num = str(v_idx + 1)
                            v_num_str = str(v_num).strip()
                            v_text = verse.text if verse.text else ""
                            self.all_bibles_data[version_name][book_name][ch_num_str][v_num_str] = f"{v_num_str}. {v_text.strip()}"
                
                if temp_ordered_books and not self.ordered_books:
                    self.ordered_books = temp_ordered_books
            except Exception as e:
                print(f"Error parsing {file}: {e}")

        if not self.ordered_books and self.all_bibles_data:
            first_ver = list(self.all_bibles_data.keys())[0]
            self.ordered_books = list(self.all_bibles_data[first_ver].keys())

    def refresh_books_grid(self):
        self.grid_content.clear_widgets()
        self.book_buttons_refs.clear()
        self.grid_content.cols = 2
        self.back_btn.disabled = True
        
        active_ver = self.version_spinner_1.text
        available_books = self.ordered_books
        if active_ver in self.all_bibles_data and self.all_bibles_data[active_ver]:
            available_books = list(self.all_bibles_data[active_ver].keys())

        for book_name in available_books:
            bg_color = [0.2, 0.2, 0.2, 1] if self.dark_mode else [0.85, 0.85, 0.85, 1]
            text_color = [1, 1, 1, 1] 
            
            display_name = book_name
            if active_ver == "BurmeseBible" and book_name in BURMESE_BOOKS:
                display_name = BURMESE_BOOKS[book_name]
            
            btn = Button(text=display_name, size_hint_y=None, height='48dp', font_size='13sp', 
                         background_color=bg_color, color=text_color)
            if FONT_PATH: btn.font_name = FONT_PATH
            btn.bind(on_press=lambda instance, b=book_name: self.on_book_selected(b))
            self.grid_content.add_widget(btn)
            self.book_buttons_refs.append(btn)

    def on_book_selected(self, book_name):
        self.selected_book = book_name
        self.grid_content.clear_widgets()
        self.book_buttons_refs.clear()
        self.grid_content.cols = 4
        self.back_btn.disabled = False
        
        active_ver = self.version_spinner_1.text
        if active_ver in self.all_bibles_data and self.selected_book in self.all_bibles_data[active_ver]:
            chapters = sorted(list(self.all_bibles_data[active_ver][self.selected_book].keys()), key=lambda x: int(x) if x.isdigit() else 0)
            for ch_num in chapters:
                bg_color = [0.25, 0.25, 0.25, 1] if self.dark_mode else [0.8, 0.8, 0.8, 1]
                text_color = [1, 1, 1, 1]
                
                btn = Button(text=str(ch_num), size_hint_y=None, height='48dp', font_size='14sp', 
                             background_color=bg_color, color=text_color)
                if FONT_PATH: btn.font_name = FONT_PATH
                btn.bind(on_press=lambda instance, c=ch_num: self.on_chapter_selected(c))
                self.grid_content.add_widget(btn)
                self.book_buttons_refs.append(btn)

    def on_chapter_selected(self, ch_num):
        self.selected_chap = ch_num
        self.show_bible_text_view()

    def go_back_to_books(self, instance):
        self.refresh_books_grid()

    def show_bible_text_view(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.text_views_container)
        self.content_area.add_widget(self.tool_bar)
        self.text_views_container.size_hint_y = 1
        
        self.update_text_views_layout()
        self.display_bible_verses()

    def show_navigation_menu(self, instance):
        if self.view1_scroll.parent:
            self.view1_scroll.parent.remove_widget(self.view1_scroll)
        if self.view2_scroll.parent:
            self.view2_scroll.parent.remove_widget(self.view2_scroll)
        if self.view1_splitter.parent:
            self.view1_splitter.parent.remove_widget(self.view1_splitter)
            
        self.text_views_container.clear_widgets()
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.nav_panel)
        self.text_views_container.size_hint_y = None
        self.text_views_container.height = 0
        self.on_book_selected(self.selected_book)

    def toggle_multi_view(self, instance):
        if instance.state == 'down':
            if self.version_spinner_2 not in self.top_bar.children:
                self.top_bar.add_widget(self.version_spinner_2)
        else:
            if self.version_spinner_2 in self.top_bar.children:
                self.top_bar.remove_widget(self.version_spinner_2)
                
        self.update_text_views_layout()
        self.display_bible_verses()

    def update_text_views_layout(self):
        if self.view1_scroll.parent:
            self.view1_scroll.parent.remove_widget(self.view1_scroll)
        if self.view2_scroll.parent:
            self.view2_scroll.parent.remove_widget(self.view2_scroll)
        if self.view1_splitter.parent:
            self.view1_splitter.parent.remove_widget(self.view1_splitter)
            
        self.text_views_container.clear_widgets()
        
        if self.multi_view_btn.state == 'down':
            self.view1_splitter.add_widget(self.view1_scroll)
            self.text_views_container.add_widget(self.view1_splitter)
            self.text_views_container.add_widget(self.view2_scroll)
        else:
            self.text_views_container.add_widget(self.view1_scroll)

    def on_version_changed(self, spinner, text):
        if self.back_btn.disabled:
            self.refresh_books_grid()
        else:
            self.on_book_selected(self.selected_book)
        self.display_bible_verses()

    def fill_text_data(self, label_widget, version_name):
        if not version_name or version_name not in self.all_bibles_data:
            label_widget.text = "Please place Bible XML files inside the 'bibles' folder."
            return

        display_book = self.selected_book
        if version_name == "BurmeseBible" and self.selected_book in BURMESE_BOOKS:
            display_book = BURMESE_BOOKS[self.selected_book]

        display_text = f"=== {display_book} (Chapter {self.selected_chap}) [{version_name}] ===\n\n"
        book_data = self.all_bibles_data[version_name].get(self.selected_book, {})
        chapter_data = book_data.get(self.selected_chap, {})
        
        if chapter_data:
            sorted_verses = sorted(list(chapter_data.keys()), key=lambda x: int(x) if x.isdigit() else 0)
            verses_list = []
            for v_key in sorted_verses:
                verses_list.append(chapter_data[v_key])
            display_text += " ".join(verses_list)  
        else:
            display_text += "This chapter/book data is empty or format mismatch."
            
        label_widget.text = display_text

    def display_bible_verses(self):
        if not self.selected_book or not self.selected_chap:
            return
        self.fill_text_data(self.text_display_1, self.version_spinner_1.text)
        if self.multi_view_btn.state == 'down':
            self.fill_text_data(self.text_display_2, self.version_spinner_2.text)

    def action_highlight(self, instance):
        lbl = Label(text='Chapter marked successfully.')
        if FONT_PATH: lbl.font_name = FONT_PATH
        popup = Popup(title='Success', content=lbl, size_hint=(0.7, 0.3))
        popup.open()

    def action_add_note(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        note_input = TextInput(hint_text="Write note here...", multiline=True)
        if FONT_PATH: note_input.font_name = FONT_PATH
        save_btn = Button(text="Save", size_hint_y=None, height='45dp', background_color=[0.12, 0.23, 0.35, 1])
        if FONT_PATH: save_btn.font_name = FONT_PATH
        box.add_widget(note_input)
        box.add_widget(save_btn)
        popup = Popup(title='Add Note', content=box, size_hint=(0.9, 0.5))
        save_btn.bind(on_press=lambda btn: popup.dismiss())
        popup.open()

    def execute_bible_search(self, instance):
        query = self.search_input.text.strip()
        active_ver = self.version_spinner_1.text
        if not query or active_ver not in self.all_bibles_data:
            return

        results = []
        for b_name, chapters in self.all_bibles_data[active_ver].items():
            for ch_num, verses in chapters.items():
                for v_num, v_text in verses.items():
                    if query.lower() in v_text.lower():
                        results.append((b_name, ch_num, v_num, v_text))

        scroll = ScrollView()
        results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        results_layout.bind(minimum_height=results_layout.setter('height'))
        
        if not results:
            lbl = Label(text=f"No results found for '{query}'", size_hint_y=None, height='40dp')
            if FONT_PATH: lbl.font_name = FONT_PATH
            results_layout.add_widget(lbl)
        else:
            for r in results:
                b_display = r[0]
                if active_ver == "BurmeseBible" and r[0] in BURMESE_BOOKS:
                    b_display = BURMESE_BOOKS[r[0]]
                    
                btn = Button(text=f"{b_display} {r[1]}:{r[2]} -> {r[3][:30]}...", size_hint_y=None, height='50dp', font_size='13sp', background_color=[0.25, 0.35, 0.45, 1])
                if FONT_PATH: btn.font_name = FONT_PATH
                btn.bind(on_press=lambda inst, b=r[0], c=r[1]: self.go_to_search_target(b, c, popup))
                results_layout.add_widget(btn)
                
        scroll.add_widget(results_layout)
        popup = Popup(title=f"Search Results ({len(results)})", content=scroll, size_hint=(0.95, 0.8))
        popup.open()

    def go_to_search_target(self, book, chapter, popup_to_close):
        popup_to_close.dismiss()
        self.selected_book = book
        self.selected_chap = chapter
        self.show_bible_text_view()

    def toggle_app_theme(self, instance):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.theme_btn.text = "Light"
            self.root_bg_color.rgba = [0.1, 0.12, 0.15, 1]
            
            self.text_display_1.bg_color.rgba = [0.06, 0.09, 0.14, 1]  
            self.text_display_1.color = [0.9, 0.95, 1, 1]              
            self.text_display_2.bg_color.rgba = [0.06, 0.09, 0.14, 1]
            self.text_display_2.color = [0.9, 0.95, 1, 1]
        else:
            self.theme_btn.text = "Dark"
            self.root_bg_color.rgba = [0.95, 0.95, 0.95, 1]
            
            self.text_display_1.bg_color.rgba = [1, 1, 1, 1]          
            self.text_display_1.color = [0, 0, 0, 1]                  
            self.text_display_2.bg_color.rgba = [1, 1, 1, 1]
            self.text_display_2.color = [0, 0, 0, 1]
            
        for btn in self.book_buttons_refs:
            if self.dark_mode:
                btn.background_color = [0.2, 0.2, 0.2, 1] if self.grid_content.cols == 2 else [0.25, 0.25, 0.25, 1]
                btn.color = [1, 1, 1, 1]
            else:
                btn.background_color = [0.85, 0.85, 0.85, 1] if self.grid_content.cols == 2 else [0.8, 0.8, 0.8, 1]
                btn.color = [1, 1, 1, 1]

if __name__ == "__main__":
    AndroidBibleApp().run()
