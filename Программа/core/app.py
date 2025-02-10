import customtkinter as ctk
import multiprocessing as multproc
import imuapp
from var import Vars

# Глобальные переменные
names_navig_frame = {'home': 'Тестирование',
                     'system': 'Система забора воды', 'test_m': 'Тест моторов'}
FONT = 'Bahnschrift'


# Класс приложения
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Инициализация приложения
        self.init_root()
        self.init_panel()
        self.init_main_page()
        self.init_module_page()
        self.init_test_motors_page()

        # Страница по умолчанию
        self.select_frame_by_names("home")

        self.init_imu_tester_window()

    def init_root(self):
        # Настройка приложения
        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("Dark")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("dark-blue")

        self.title('Настройки квадрокоптера')
        self.geometry('700x500')
        self.resizable(False, False)

    def init_imu_tester_window(self):
        Vars['imuapp_is_enabled'] = False
        # Var.imuapp.is_enabled=False

    def init_panel(self):
        # Настройки панели слева
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=names_navig_frame['home'], fg_color="transparent", text_color=(
            "gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", font=(FONT, 16), command=lambda: self.select_frame_by_names('home'))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=names_navig_frame["system"], fg_color="transparent", text_color=(
            "gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", font=(FONT, 16), command=lambda: self.select_frame_by_names('system'))
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=names_navig_frame["test_m"], fg_color="transparent", text_color=(
            "gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", font=(FONT, 16), command=lambda: self.select_frame_by_names('test_m'))
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, font=(
            FONT, 16), values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

    def init_main_page(self):
        # Главная страница
        self.home_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.home_frame, text="Пульт управления", fg_color="transparent", font=(
            FONT, 16)).grid(row=0, column=0, pady=10, padx=30, sticky="W")

        self.slider1_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider1_l.grid(row=1, column=0, pady=10, padx=5, sticky="e")
        self.slider1_r = ctk.CTkProgressBar(self.home_frame)
        self.slider1_r.grid(row=1, column=1, pady=10)

        self.slider2_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider2_l.grid(row=2, column=0, pady=10, padx=5, sticky="e")
        self.slider2_r = ctk.CTkProgressBar(self.home_frame)
        self.slider2_r.grid(row=2, column=1, pady=10)

        self.slider3_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider3_l.grid(row=3, column=0, pady=10, padx=5, sticky="e")
        self.slider3_r = ctk.CTkProgressBar(self.home_frame)
        self.slider3_r.grid(row=3, column=1, pady=10)

        self.slider4_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider4_l.grid(row=4, column=0, pady=10, padx=5, sticky="e")
        self.slider4_r = ctk.CTkProgressBar(self.home_frame)
        self.slider4_r.grid(row=4, column=1, pady=10)

        self.slider5_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider5_l.grid(row=5, column=0, pady=10, padx=5, sticky="e")
        self.slider5_r = ctk.CTkProgressBar(self.home_frame)
        self.slider5_r.grid(row=5, column=1, pady=10)

        self.slider6_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider6_l.grid(row=6, column=0, pady=10, padx=5, sticky="e")
        self.slider6_r = ctk.CTkProgressBar(self.home_frame)
        self.slider6_r.grid(row=6, column=1, pady=10)

        self.slider7_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider7_l.grid(row=7, column=0, pady=10, padx=5, sticky="e")
        self.slider7_r = ctk.CTkProgressBar(self.home_frame)
        self.slider7_r.grid(row=7, column=1, pady=10)

        self.slider8_l = ctk.CTkProgressBar(
            self.home_frame, fg_color="#1f538d", progress_color='grey30')
        self.slider8_l.grid(row=8, column=0, pady=10, padx=5, sticky="e")
        self.slider8_r = ctk.CTkProgressBar(self.home_frame)
        self.slider8_r.grid(row=8, column=1, pady=10)

        self.imu_button = ctk.CTkButton(self.home_frame, height=40, border_spacing=10, text="Тест IMU - сенсора", text_color=(
            "gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="center", font=(FONT, 16), command=self.start_imu_test)
        self.imu_button.grid(row=9, column=0, columnspan=3,
                             padx=50, pady=20, sticky="ew")

        # self.slider1_l.set(0.75)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=2)

    def init_module_page(self):
        # Страница системы забора воды
        self.second_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.second_frame, text="Настройка системы", fg_color="transparent", font=(
            FONT, 16)).grid(row=0, column=0, pady=10, padx=30, sticky="W")

    def init_module_page(self):
        # Страница системы забора воды
        self.second_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.second_frame, text="Настройка системы", fg_color="transparent", font=(
            FONT, 16)).grid(row=0, column=0, pady=10, padx=30, sticky="W")

    def init_test_motors_page(self):
        # Страница теста моторов
        self.third_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.third_frame, text="Тест моторов", fg_color="transparent", font=(
            FONT, 16)).grid(row=0, column=0, pady=10, padx=30, sticky="W")
        self.slider_m = ctk.CTkSlider(
            self.third_frame, from_=0, to=255, width=450)
        self.slider_m.grid(row=1, column=0, pady=10, columnspan=3)

    # Функции
    def start_imu_test(self):
        print(Vars['imuapp_is_enabled'])
        if not Vars['imuapp_is_enabled']:
            self.imuapp = multproc.Process(target=imuapp.start)
            self.imuapp.start()
            # self.imuapp.join()

        # self.destroy()
        # os.startfile(r"IMU_test\forproccesing.exe")
        # os.system(r"javac IMU_test\source\IMU_watching.java")
        # subprocess.run([r"IMU_test\IMU_test.exe"])

    def select_frame_by_names(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "system" else "transparent")
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "test_m" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "system":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "test_m":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
