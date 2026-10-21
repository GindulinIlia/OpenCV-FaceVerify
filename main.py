import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Window.size = (480, 844)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

Builder.load_file(os.path.join(BASE_DIR, 'main.kv'))

PROGRAMS_DATA = {
    'architecture': {
        'code': '07.03.01',
        'name': 'Архитектура',
        'subjects': [
            ('Русский язык', 40, 100),
            ('Математика', 40, 100),
            ('Рисунок', 40, 100),
        ]
    },
    'design': {
        'code': '54.03.01',
        'name': 'Дизайн',
        'subjects': [
            ('Русский язык', 40, 100),
            ('Литература', 40, 100),
            ('Рисунок', 40, 100),
        ]
    },
    'service': {
        'code': '43.03.01',
        'name': 'Сервис',
        'subjects': [
            ('Русский язык', 40, 100),
            ('Обществознание', 45, 100),
            ('Математика', 40, 100),
            ('История', 36, 100),
            ('География', 40, 100),
            ('Иностранный язык', 30, 100),
        ]
    },
    'construction': {
        'code': '08.03.01',
        'name': 'Строительство',
        'subjects': [
            ('Русский язык', 40, 100),
            ('Математика', 40, 100),
            ('Информатика', 44, 100),
            ('Физика', 39, 100),
        ]
    },
    'information': {
        'code': '09.03.03',
        'name': 'Прикладная информатика',
        'subjects': [
            ('Русский язык', 40, 100),
            ('Математика', 40, 100),
            ('Информатика', 44, 100),
            ('Физика', 39, 100),
        ]
    }
}


class MainScreen(Screen):
    def go_to_direction(self, direction_name, direction_id):
        print(f"Переход на: {direction_name} (id={direction_id})")
        next_screen = self.manager.get_screen(direction_name)
        next_screen.direction_id = direction_id
        next_screen.direction_name = PROGRAMS_DATA[direction_name]['name']
        next_screen.populate_table()
        self.manager.current = direction_name


class DirectionScreen(Screen):
    direction_id = 0
    direction_name = ""

    def go_back(self):
        self.manager.current = 'main'

    def populate_table(self):
        key = self.name
        if key not in PROGRAMS_DATA:
            return
        container = self.ids.table_container
        container.clear_widgets()
        data = PROGRAMS_DATA[key]
        self._build_table(container, data)

    def _build_table(self, container, data):
        table_wrapper = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),
            padding=dp(2)
        )
        table_wrapper.bind(minimum_height=table_wrapper.setter('height'))

        code = data['code']
        subjects = data['subjects']
        row_height = dp(40)
        header_height = dp(45)
        total_height = header_height + len(subjects) * row_height + dp(50)
        table_wrapper.height = total_height

        header = BoxLayout(size_hint_y=None, height=header_height)
        header_cols = [
            ('Код', 0.2),
            ('Вступительные испытания по ЕГЭ', 0.45),
            ('Мин. баллов', 0.175),
            ('Макс. баллов', 0.175)
        ]
        for col_text, col_width in header_cols:
            lbl = Label(
                text=col_text.upper(),
                bold=True,
                color=(0.173, 0.243, 0.314, 1),
                size_hint_x=col_width,
                font_size=dp(12)
            )
            header.add_widget(lbl)
        table_wrapper.add_widget(header)

        for i, (subject, min_score, max_score) in enumerate(subjects):
            row = BoxLayout(size_hint_y=None, height=row_height)

            if i == 0:
                code_lbl = Label(
                    text=code,
                    size_hint_x=0.2,
                    bold=True,
                    color=(0.173, 0.243, 0.314, 1),
                    font_size=dp(14)
                )
            else:
                code_lbl = Label(text='', size_hint_x=0.2)
            row.add_widget(code_lbl)

            subj_lbl = Label(
                text=subject,
                size_hint_x=0.45,
                color=(0.2, 0.2, 0.2, 1),
                font_size=dp(14),
                halign='left'
            )
            subj_lbl.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))
            row.add_widget(subj_lbl)

            min_lbl = Label(
                text=str(min_score),
                size_hint_x=0.175,
                color=(0.2, 0.2, 0.2, 1),
                font_size=dp(14),
                halign='center'
            )
            row.add_widget(min_lbl)

            max_lbl = Label(
                text=str(max_score),
                size_hint_x=0.175,
                color=(0.2, 0.2, 0.2, 1),
                font_size=dp(14),
                halign='center'
            )
            row.add_widget(max_lbl)

            table_wrapper.add_widget(row)

        container.add_widget(table_wrapper)


class ArchitectureScreen(DirectionScreen):
    pass

class DesignScreen(DirectionScreen):
    pass

class ServiceScreen(DirectionScreen):
    pass

class ConstructionScreen(DirectionScreen):
    pass

class InformationScreen(DirectionScreen):
    pass


class UniversityApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ArchitectureScreen(name='architecture'))
        sm.add_widget(DesignScreen(name='design'))
        sm.add_widget(ServiceScreen(name='service'))
        sm.add_widget(ConstructionScreen(name='construction'))
        sm.add_widget(InformationScreen(name='information'))
        return sm


if __name__ == '__main__':
    UniversityApp().run()