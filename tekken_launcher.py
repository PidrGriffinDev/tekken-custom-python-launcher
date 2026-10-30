import customtkinter as ctk
import os
import subprocess
import json
import re
from PIL import Image
from tkinter import messagebox, filedialog

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Тексты на трех языках
TEXTS = {
    "ru": {
        "title": "Tekken 3 Expanded / PLAYSTATION",
        "settings": "Настройки",
        "mods": "Моды",
        "play": "PLAY",
        "back": "< Назад",
        "disc": "Диск",
        "disc_verified": "Диск проверен",
        "change_disc": "Сменить диск",
        "player": "ИГРОК",
        "analog": "Аналог",
        "dpad": "D-Pad",
        "configure": "Настроить",
        "keyboard": "Клавиатура",
        "none": "Нет",
        "memory_card": "Карта памяти",
        "browse": "Обзор",
        "new": "Новая",
        "display": "Экран",
        "audio": "Аудио",
        "hotkeys": "Горячие клавиши",
        "window_size": "Размер окна",
        "renderer": "Рендер",
        "supersampling": "Суперсэмплинг",
        "fullscreen": "Полный экран",
        "view_mode": "Режим",
        "volume": "Громкость",
        "sample_rate": "Частота дискретизации",
        "bios": "BIOS",
        "save": "Сохранить",
        "ready": "ГОТОВ К ЗАПУСКУ",
        "starting": "ЗАПУСК ИГРЫ...",
        "not_found": "ИГРА НЕ НАЙДЕНА"
    },
    "en": {
        "title": "Tekken 3 Expanded / PLAYSTATION",
        "settings": "Settings",
        "mods": "Mods",
        "play": "PLAY",
        "back": "< Back",
        "disc": "Disc",
        "disc_verified": "Disc verified",
        "change_disc": "Change Disc",
        "player": "PLAYER",
        "analog": "Analog",
        "dpad": "D-Pad",
        "configure": "Configure",
        "keyboard": "Keyboard",
        "none": "None",
        "memory_card": "Memory Card",
        "browse": "Browse",
        "new": "New",
        "display": "Display",
        "audio": "Audio",
        "hotkeys": "Hotkeys",
        "window_size": "Window size",
        "renderer": "Renderer",
        "supersampling": "Supersampling",
        "fullscreen": "Fullscreen",
        "view_mode": "View mode",
        "volume": "Volume",
        "sample_rate": "Sample rate",
        "bios": "BIOS",
        "save": "Save",
        "ready": "READY TO PLAY",
        "starting": "STARTING GAME...",
        "not_found": "GAME NOT FOUND"
    },
    "es": {
        "title": "Tekken 3 Expanded / PLAYSTATION",
        "settings": "Configuración",
        "mods": "Mods",
        "play": "PLAY",
        "back": "< Volver",
        "disc": "Disco",
        "disc_verified": "Disco verificado",
        "change_disc": "Cambiar disco",
        "player": "JUGADOR",
        "analog": "Analógico",
        "dpad": "D-Pad",
        "configure": "Configurar",
        "keyboard": "Teclado",
        "none": "Ninguno",
        "memory_card": "Tarjeta de memoria",
        "browse": "Examinar",
        "new": "Nuevo",
        "display": "Pantalla",
        "audio": "Audio",
        "hotkeys": "Atajos",
        "window_size": "Tamaño ventana",
        "renderer": "Renderizador",
        "supersampling": "Sobremuestreo",
        "fullscreen": "Pantalla completa",
        "view_mode": "Modo vista",
        "volume": "Volumen",
        "sample_rate": "Tasa muestreo",
        "bios": "BIOS",
        "save": "Guardar",
        "ready": "LISTO PARA JUGAR",
        "starting": "INICIANDO JUEGO...",
        "not_found": "JUEGO NO ENCONTRADO"
    }
}

class TekkenLauncher:
    def __init__(self):
        # Загрузка настроек
        self.settings = self.load_settings()
        self.current_lang = self.settings.get("language", "en")
        self.key_bindings = self.load_key_bindings()

        # Создаем главное окно
        self.root = ctk.CTk()
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        self.root.title("Tekken 3 Expanded Launcher")

        # Глубокий темно-серый фон
        self.root.configure(fg_color="#1a1a24")

        # Главный контейнер
        self.main_container = ctk.CTkFrame(self.root, fg_color="#1a1a24")
        self.main_container.pack(fill="both", expand=True)

        # Создаем главный экран
        self.create_main_screen()

        # Контейнер для настроек (скрыт по умолчанию)
        self.settings_container = ctk.CTkFrame(self.root, fg_color="#1a1a24")

    def create_main_screen(self):
        """Создает главный экран лаунчера"""
        # Хедер с неоновой линией
        self.header_frame = ctk.CTkFrame(
            self.main_container,
            height=60,
            fg_color="#1a1a24",
            border_width=2,
            border_color="#00d2ff",
            corner_radius=0
        )
        self.header_frame.pack(fill="x", side="top")

        # Логотип PS и надпись
        header_left = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_left.pack(side="left", padx=20, pady=10)

        ps_label = ctk.CTkLabel(
            header_left,
            text="PS",
            font=("Arial", 24, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        ps_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            header_left,
            text=TEXTS[self.current_lang]["title"],
            font=("Arial", 16, "bold"),
            text_color="#ffffff",
            fg_color="transparent"
        )
        title_label.pack(side="left")

        # Кнопки Settings, Mods и Language справа
        header_right = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_right.pack(side="right", padx=20, pady=10)

        lang_display = {"ru": "RU", "en": "EN", "es": "ES"}
        self.language_btn = ctk.CTkButton(
            header_right,
            text=f"{lang_display[self.current_lang]}",
            width=60,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.toggle_language
        )
        self.language_btn.pack(side="right", padx=5)

        self.settings_btn = ctk.CTkButton(
            header_right,
            text=TEXTS[self.current_lang]["settings"],
            width=100,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.open_settings_screen
        )
        self.settings_btn.pack(side="right", padx=5)

        self.mods_btn = ctk.CTkButton(
            header_right,
            text=TEXTS[self.current_lang]["mods"],
            width=100,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.show_mods_message
        )
        self.mods_btn.pack(side="right", padx=5)

        # Основной контент
        content_frame = ctk.CTkFrame(self.main_container, fg_color="#1a1a24")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Левый блок - информация о диске
        self.disc_frame = ctk.CTkFrame(
            content_frame,
            width=350,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        self.disc_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        disc_title = ctk.CTkLabel(
            self.disc_frame,
            text=TEXTS[self.current_lang]["disc"],
            font=("Arial", 18, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        disc_title.pack(pady=(15, 10))

        # Обложка диска (заглушка)
        disc_cover = ctk.CTkFrame(
            self.disc_frame,
            width=200,
            height=200,
            fg_color="#2a2a35",
            corner_radius=8
        )
        disc_cover.pack(pady=10)

        disc_cover_label = ctk.CTkLabel(
            disc_cover,
            text="TEKKEN 3",
            font=("Arial", 20, "bold"),
            text_color="#ffffff",
            fg_color="transparent"
        )
        disc_cover_label.place(relx=0.5, rely=0.5, anchor="center")

        disc_status = ctk.CTkLabel(
            self.disc_frame,
            text=TEXTS[self.current_lang]["disc_verified"],
            font=("Arial", 12),
            text_color="#00ff00",
            fg_color="transparent"
        )
        disc_status.pack(pady=5)

        serial_label = ctk.CTkLabel(
            self.disc_frame,
            text="SLUS-00402",
            font=("Arial", 11),
            text_color="#888888",
            fg_color="transparent"
        )
        serial_label.pack(pady=(0, 10))

        change_disc_btn = ctk.CTkButton(
            self.disc_frame,
            text=TEXTS[self.current_lang]["change_disc"],
            width=200,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.change_disc
        )
        change_disc_btn.pack(pady=(0, 15))

        # Правый блок
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True)

        # PLAYER 1 блок
        self.player1_frame = ctk.CTkFrame(
            right_frame,
            height=200,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        self.player1_frame.pack(fill="x", pady=(0, 10))

        player1_header = ctk.CTkFrame(self.player1_frame, fg_color="transparent")
        player1_header.pack(fill="x", padx=15, pady=10)

        player1_label = ctk.CTkLabel(
            player1_header,
            text=f"{TEXTS[self.current_lang]['player']} 1",
            font=("Arial", 16, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        player1_label.pack(side="left")

        # Картинка геймпада PLAYER 1
        self.load_gamepad_image(self.player1_frame, "player1")

        # PLAYER 2 блок
        self.player2_frame = ctk.CTkFrame(
            right_frame,
            height=200,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        self.player2_frame.pack(fill="x", pady=(0, 10))

        player2_header = ctk.CTkFrame(self.player2_frame, fg_color="transparent")
        player2_header.pack(fill="x", padx=15, pady=10)

        player2_label = ctk.CTkLabel(
            player2_header,
            text=f"{TEXTS[self.current_lang]['player']} 2",
            font=("Arial", 16, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        player2_label.pack(side="left")

        # Картинка геймпада PLAYER 2
        self.load_gamepad_image(self.player2_frame, "player2")

        # Memory Cards блок
        memory_frame = ctk.CTkFrame(
            right_frame,
            height=120,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        memory_frame.pack(fill="x")

        memory_title = ctk.CTkLabel(
            memory_frame,
            text=TEXTS[self.current_lang]["memory_card"],
            font=("Arial", 14, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        memory_title.pack(pady=(10, 5))

        memory_cards = ctk.CTkFrame(memory_frame, fg_color="transparent")
        memory_cards.pack(fill="x", padx=15, pady=5)

        # Card 1
        card1_frame = ctk.CTkFrame(memory_cards, fg_color="transparent")
        card1_frame.pack(side="left", expand=True)

        card1_label = ctk.CTkLabel(
            card1_frame,
            text="card1.mcd",
            font=("Arial", 11),
            text_color="#ffffff",
            fg_color="transparent"
        )
        card1_label.pack(side="left", padx=5)

        browse1_btn = ctk.CTkButton(
            card1_frame,
            text=TEXTS[self.current_lang]["browse"],
            width=60,
            height=25,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=5,
            font=("Arial", 10),
            command=lambda: self.browse_memory_card("card1")
        )
        browse1_btn.pack(side="left", padx=5)

        new1_btn = ctk.CTkButton(
            card1_frame,
            text=TEXTS[self.current_lang]["new"],
            width=60,
            height=25,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=5,
            font=("Arial", 10),
            command=lambda: self.create_memory_card("card1")
        )
        new1_btn.pack(side="left", padx=5)

        # Card 2
        card2_frame = ctk.CTkFrame(memory_cards, fg_color="transparent")
        card2_frame.pack(side="left", expand=True)

        card2_label = ctk.CTkLabel(
            card2_frame,
            text="card2.mcd",
            font=("Arial", 11),
            text_color="#ffffff",
            fg_color="transparent"
        )
        card2_label.pack(side="left", padx=5)

        browse2_btn = ctk.CTkButton(
            card2_frame,
            text=TEXTS[self.current_lang]["browse"],
            width=60,
            height=25,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=5,
            font=("Arial", 10),
            command=lambda: self.browse_memory_card("card2")
        )
        browse2_btn.pack(side="left", padx=5)

        new2_btn = ctk.CTkButton(
            card2_frame,
            text=TEXTS[self.current_lang]["new"],
            width=60,
            height=25,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=5,
            font=("Arial", 10),
            command=lambda: self.create_memory_card("card2")
        )
        new2_btn.pack(side="left", padx=5)

        # Кнопка PLAY внизу справа
        play_btn = ctk.CTkButton(
            self.main_container,
            text=f"▶ {TEXTS[self.current_lang]['play']}",
            font=("Arial", 20, "bold"),
            width=200,
            height=60,
            fg_color="#0066cc",
            hover_color="#0077ee",
            text_color="#ffffff",
            corner_radius=10,
            command=self.start_game
        )
        play_btn.place(relx=0.95, rely=0.92, anchor="center")

    def load_gamepad_image(self, parent_frame, player_id):
        """Загружает и отображает картинку геймпада"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gamepad_path = os.path.join(script_dir, "gamepad.png")

        try:
            if os.path.exists(gamepad_path):
                gamepad_image = Image.open(gamepad_path)
                gamepad_ctk = ctk.CTkImage(
                    light_image=gamepad_image,
                    dark_image=gamepad_image,
                    size=(80, 60)
                )

                gamepad_label = ctk.CTkLabel(
                    parent_frame,
                    image=gamepad_ctk,
                    text="",
                    fg_color="transparent"
                )
                gamepad_label.place(relx=0.85, rely=0.5, anchor="center")
            else:
                # Заглушка если картинки нет
                placeholder = ctk.CTkLabel(
                    parent_frame,
                    text="🎮",
                    font=("Arial", 30),
                    text_color="#4a4a5a",
                    fg_color="transparent"
                )
                placeholder.place(relx=0.85, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Error loading gamepad: {e}")

    def open_settings_screen(self):
        """Открывает экран настроек"""
        # Скрываем главный экран
        self.main_container.pack_forget()

        # Показываем настройки
        self.settings_container.pack(fill="both", expand=True)
        self.create_settings_screen()

    def create_settings_screen(self):
        """Создает экран настроек"""
        # Хедер настроек
        settings_header = ctk.CTkFrame(
            self.settings_container,
            height=60,
            fg_color="#1a1a24",
            border_width=2,
            border_color="#00d2ff",
            corner_radius=0
        )
        settings_header.pack(fill="x", side="top")

        settings_title = ctk.CTkLabel(
            settings_header,
            text=TEXTS[self.current_lang]["settings"],
            font=("Arial", 20, "bold"),
            text_color="#ffffff",
            fg_color="transparent"
        )
        settings_title.pack(side="left", padx=20, pady=15)

        back_btn = ctk.CTkButton(
            settings_header,
            text=TEXTS[self.current_lang]["back"],
            width=100,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.back_to_main
        )
        back_btn.pack(side="right", padx=20, pady=10)

        # Контент настроек
        settings_content = ctk.CTkFrame(self.settings_container, fg_color="#1a1a24")
        settings_content.pack(fill="both", expand=True, padx=20, pady=20)

        # DISPLAY блок
        display_frame = ctk.CTkFrame(
            settings_content,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        display_frame.pack(fill="x", pady=(0, 10))

        display_title = ctk.CTkLabel(
            display_frame,
            text=TEXTS[self.current_lang]["display"],
            font=("Arial", 16, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        display_title.pack(pady=10, padx=15, anchor="w")

        # Window size
        size_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=15, pady=5)

        size_label = ctk.CTkLabel(
            size_frame,
            text=TEXTS[self.current_lang]["window_size"],
            font=("Arial", 12),
            text_color="#ffffff",
            fg_color="transparent",
            width=150
        )
        size_label.pack(side="left")

        self.window_size_var = ctk.StringVar(value="1280x960")
        size_menu = ctk.CTkOptionMenu(
            size_frame,
            variable=self.window_size_var,
            values=["1280x720", "1280x960", "1920x1080"],
            width=200
        )
        size_menu.pack(side="left", padx=10)

        # Renderer
        renderer_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        renderer_frame.pack(fill="x", padx=15, pady=5)

        renderer_label = ctk.CTkLabel(
            renderer_frame,
            text=TEXTS[self.current_lang]["renderer"],
            font=("Arial", 12),
            text_color="#ffffff",
            fg_color="transparent",
            width=150
        )
        renderer_label.pack(side="left")

        self.renderer_var = ctk.StringVar(value="OpenGL")
        renderer_menu = ctk.CTkOptionMenu(
            renderer_frame,
            variable=self.renderer_var,
            values=["OpenGL", "Software"],
            width=200
        )
        renderer_menu.pack(side="left", padx=10)

        # AUDIO блок
        audio_frame = ctk.CTkFrame(
            settings_content,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        audio_frame.pack(fill="x", pady=(0, 10))

        audio_title = ctk.CTkLabel(
            audio_frame,
            text=TEXTS[self.current_lang]["audio"],
            font=("Arial", 16, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        audio_title.pack(pady=10, padx=15, anchor="w")

        # Volume
        volume_frame = ctk.CTkFrame(audio_frame, fg_color="transparent")
        volume_frame.pack(fill="x", padx=15, pady=5)

        volume_label = ctk.CTkLabel(
            volume_frame,
            text=TEXTS[self.current_lang]["volume"],
            font=("Arial", 12),
            text_color="#ffffff",
            fg_color="transparent",
            width=150
        )
        volume_label.pack(side="left")

        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            number_of_steps=20,
            width=300
        )
        self.volume_slider.set(80)
        self.volume_slider.pack(side="left", padx=10)

        # HOTKEYS блок
        hotkeys_frame = ctk.CTkFrame(
            settings_content,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        hotkeys_frame.pack(fill="x", pady=(0, 10))

        hotkeys_title = ctk.CTkLabel(
            hotkeys_frame,
            text=TEXTS[self.current_lang]["hotkeys"],
            font=("Arial", 16, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        hotkeys_title.pack(pady=10, padx=15, anchor="w")

        configure_btn = ctk.CTkButton(
            hotkeys_frame,
            text=TEXTS[self.current_lang]["configure"],
            width=200,
            height=35,
            fg_color="#4a4a5a",
            hover_color="#5a5a6a",
            text_color="#ffffff",
            corner_radius=8,
            command=self.open_keyboard_config
        )
        configure_btn.pack(pady=10, padx=15, anchor="w")

        # Кнопка сохранения
        save_btn = ctk.CTkButton(
            settings_content,
            text=TEXTS[self.current_lang]["save"],
            width=150,
            height=40,
            fg_color="#0066cc",
            hover_color="#0077ee",
            text_color="#ffffff",
            corner_radius=10,
            command=self.save_all_settings
        )
        save_btn.pack(pady=10, anchor="e")

    def back_to_main(self):
        """Возврат на главный экран"""
        self.settings_container.pack_forget()
        self.main_container.pack(fill="both", expand=True)

    def toggle_language(self):
        """Циклическое переключение языка (RU -> EN -> ES -> RU)"""
        languages = ["ru", "en", "es"]
        current_idx = languages.index(self.current_lang)
        self.current_lang = languages[(current_idx + 1) % len(languages)]
        self.settings["language"] = self.current_lang
        self.save_settings()
        self.update_texts()

    def update_texts(self):
        """Обновление всех текстов на интерфейсе"""
        # Обновляем хедер
        lang_display = {"ru": "RU", "en": "EN", "es": "ES"}
        self.language_btn.configure(text=f"{lang_display[self.current_lang]}")
        self.settings_btn.configure(text=TEXTS[self.current_lang]["settings"])
        self.mods_btn.configure(text=TEXTS[self.current_lang]["mods"])

        # Обновляем главный экран
        title_label = self.header_frame.winfo_children()[1].winfo_children()[1]
        title_label.configure(text=TEXTS[self.current_lang]["title"])

        # Обновляем play кнопку
        play_btn = self.main_container.winfo_children()[-1]
        play_btn.configure(text=f"▶ {TEXTS[self.current_lang]['play']}")

        # Пересоздаем главный экран для обновления всех текстов
        self.main_container.pack_forget()
        self.main_container = ctk.CTkFrame(self.root, fg_color="#1a1a24")
        self.main_container.pack(fill="both", expand=True)
        self.create_main_screen()

    def change_disc(self):
        """Открывает диалог для выбора диска (.cue файл)"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = filedialog.askopenfilename(
            title=TEXTS[self.current_lang]["change_disc"],
            initialdir=script_dir,
            filetypes=[("CUE files", "*.cue"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", f"Выбран диск: {os.path.basename(file_path)}")

    def browse_memory_card(self, card_name):
        """Открывает диалог для выбора карты памяти (.mcd/.srm файл)"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = filedialog.askopenfilename(
            title=f"Browse {card_name}",
            initialdir=script_dir,
            filetypes=[("Memory Card files", "*.mcd *.srm"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", f"Выбрана карта: {os.path.basename(file_path)}")

    def create_memory_card(self, card_name):
        """Создает новый пустой файл карты памяти"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        card_file = os.path.join(script_dir, f"{card_name}.mcd")

        if os.path.exists(card_file):
            messagebox.showwarning("Warning", f"Файл {card_name}.mcd уже существует!")
            return

        try:
            # Создаем пустой файл карты памяти (128KB - стандартный размер PS1)
            with open(card_file, 'wb') as f:
                f.write(b'\x00' * (128 * 1024))
            messagebox.showinfo("Success", f"Создана новая карта памяти: {card_name}.mcd")
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось создать карту памяти: {e}")

    def show_mods_message(self):
        """Показывает уведомление что моды в разработке"""
        messagebox.showinfo("Mods", "Раздел в разработке!\nМенеджер модов появится в следующем обновлении лаунчера.")

    def open_keyboard_config(self):
        """Открывает окно настройки клавиатуры"""
        kb_window = ctk.CTkToplevel(self.root)
        kb_window.title(TEXTS[self.current_lang]["hotkeys"])
        kb_window.geometry("400x500")
        kb_window.resizable(False, False)
        kb_window.configure(fg_color="#1a1a24")

        title = ctk.CTkLabel(
            kb_window,
            text=TEXTS[self.current_lang]["hotkeys"],
            font=("Arial", 18, "bold"),
            text_color="#00d2ff",
            fg_color="transparent"
        )
        title.pack(pady=15)

        keys_frame = ctk.CTkFrame(
            kb_window,
            fg_color="#252530",
            corner_radius=12,
            border_width=1,
            border_color="#3a3a4a"
        )
        keys_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.key_vars = {}
        key_labels = ["up", "down", "left", "right", "button1", "button2", "button3", "button4"]
        key_names = [TEXTS[self.current_lang][k] for k in key_labels]

        for i, (key, name) in enumerate(zip(key_labels, key_names)):
            label = ctk.CTkLabel(
                keys_frame,
                text=name,
                font=("Arial", 12),
                text_color="#ffffff",
                fg_color="transparent",
                width=120
            )
            label.grid(row=i, column=0, padx=10, pady=8, sticky="w")

            key_var = ctk.StringVar(value=self.key_bindings.get(key, ""))
            self.key_vars[key] = key_var

            entry = ctk.CTkEntry(
                keys_frame,
                textvariable=key_var,
                width=80,
                fg_color="#1a1a24",
                border_color="#3a3a4a",
                border_width=1,
                text_color="#ffffff",
                font=("Arial", 11)
            )
            entry.grid(row=i, column=1, padx=10, pady=8)

        save_kb_btn = ctk.CTkButton(
            kb_window,
            text=TEXTS[self.current_lang]["save"],
            width=150,
            height=40,
            fg_color="#0066cc",
            hover_color="#0077ee",
            text_color="#ffffff",
            corner_radius=10,
            command=lambda: self.save_key_settings(kb_window)
        )
        save_kb_btn.pack(pady=15)

    def load_settings(self):
        """Загрузка настроек"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, "launcher_settings.json")
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"language": "en"}

    def save_settings(self):
        """Сохранение настроек"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, "launcher_settings.json")
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def load_key_bindings(self):
        """Загрузка настроек клавиатуры из game.toml"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        game_toml = os.path.join(script_dir, "game.toml")

        defaults = {
            "up": "W",
            "down": "S",
            "left": "A",
            "right": "D",
            "button1": "J",
            "button2": "K",
            "button3": "L",
            "button4": "I"
        }

        if os.path.exists(game_toml):
            try:
                with open(game_toml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    keyboard_section = re.search(r'\[(?:keyboard|controller)\](.*?)(?=\n\[|\Z)', content, re.DOTALL)
                    if keyboard_section:
                        for line in keyboard_section.group(1).split('\n'):
                            match = re.match(r'(\w+)\s*=\s*["\']?([a-zA-Z0-9])["\']?', line)
                            if match:
                                key, value = match.groups()
                                if key in defaults:
                                    defaults[key] = value.upper()
            except:
                pass

        return defaults

    def save_key_bindings(self, bindings):
        """Сохранение настроек клавиатуры в game.toml"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        game_toml = os.path.join(script_dir, "game.toml")

        if os.path.exists(game_toml):
            try:
                with open(game_toml, 'r', encoding='utf-8') as f:
                    content = f.read()

                keyboard_keys = ["up", "down", "left", "right", "button1", "button2", "button3", "button4"]

                if "[keyboard]" in content:
                    for key in keyboard_keys:
                        pattern = rf'{key}\s*=\s*["\']?[a-zA-Z0-9]["\']?'
                        replacement = f'{key} = "{bindings[key]}"'
                        content = re.sub(pattern, replacement, content)
                else:
                    keyboard_section = "\n[keyboard]\n"
                    for key in keyboard_keys:
                        keyboard_section += f'{key} = "{bindings[key]}"\n'
                    content += keyboard_section

                with open(game_toml, 'w', encoding='utf-8') as f:
                    f.write(content)

                return True
            except Exception as e:
                print(f"Error saving key bindings: {e}")
                return False
        return False

    def save_key_settings(self, window):
        """Сохранение настроек клавиатуры"""
        new_bindings = {}
        for key, var in self.key_vars.items():
            new_bindings[key] = var.get().upper()

        if self.save_key_bindings(new_bindings):
            self.key_bindings = new_bindings
            messagebox.showinfo("Success", "Настройки сохранены!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Не удалось сохранить настройки")

    def save_all_settings(self):
        """Сохранение всех настроек"""
        messagebox.showinfo("Success", "Все настройки сохранены!")

    def start_game(self):
        """Запуск игры"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        game_exe = os.path.join(script_dir, "Tekken 3 Expanded.exe")

        if os.path.exists(game_exe):
            try:
                subprocess.Popen([game_exe], cwd=script_dir)
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Ошибка запуска: {e}")
        else:
            messagebox.showerror("Error", TEXTS[self.current_lang]["not_found"])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TekkenLauncher()
    app.run()
