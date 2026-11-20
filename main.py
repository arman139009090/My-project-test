from datetime import datetime

import jdatetime
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

BG = (0.063, 0.063, 0.110, 1)
CARD = (0.114, 0.114, 0.188, 1)
INPUT_BG = (0.161, 0.161, 0.251, 1)
PURPLE = (0.608, 0.447, 1, 1)
WHITE = (1, 1, 1, 1)
GRAY = (0.647, 0.647, 0.741, 1)
CYAN = (0.439, 0.839, 1, 1)

Window.clearcolor = BG


def lbl(text, size, color, bold=True, height=None):
    l = Label(text=text, font_size=sp(size), color=color, bold=bold,
              halign="center", valign="middle", size_hint_y=None,
              height=height or dp(size * 2.2))
    l.bind(size=lambda w, s: setattr(w, "text_size", s))
    return l


class AgeApp(App):
    title = "Age Calculator"
    birth_date = None

    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(8))

        root.add_widget(lbl("AGE CALCULATOR", 24, PURPLE))
        root.add_widget(lbl("Discover your exact age", 12, GRAY, bold=False))

        card = BoxLayout(orientation="vertical", padding=dp(16),
                         spacing=dp(6), size_hint_y=None, height=dp(300))
        from kivy.graphics import Color, RoundedRectangle
        with card.canvas.before:
            Color(*CARD)
            self._rect = RoundedRectangle(radius=[dp(14)])
        card.bind(pos=lambda w, v: setattr(self._rect, "pos", v),
                  size=lambda w, v: setattr(self._rect, "size", v))

        card.add_widget(lbl("DATE OF BIRTH", 16, WHITE))
        self.entries = []
        for title, ph in [("Birth Year (Jalali)", "1390"),
                          ("Birth Month", "12"),
                          ("Birth Day", "10")]:
            card.add_widget(lbl(title, 12, GRAY, bold=False, height=dp(22)))
            e = TextInput(text=ph, multiline=False, input_filter="int",
                          halign="center", font_size=sp(18),
                          background_normal="", background_active="",
                          background_color=INPUT_BG, foreground_color=WHITE,
                          cursor_color=WHITE, size_hint_y=None,
                          height=dp(44), padding=[0, dp(10)])
            card.add_widget(e)
            self.entries.append(e)
        root.add_widget(card)

        root.add_widget(lbl("YOUR CURRENT AGE", 14, GRAY))
        self.age_display = lbl("--", 26, PURPLE)
        root.add_widget(self.age_display)
        self.detail_display = lbl("Enter your date of birth", 13, WHITE,
                                  bold=False, height=dp(60))
        root.add_widget(self.detail_display)
        self.clock_display = lbl("", 13, CYAN)
        root.add_widget(self.clock_display)

        btn = Button(text="CALCULATE AGE", bold=True, font_size=sp(16),
                     background_normal="", background_color=PURPLE,
                     color=WHITE, size_hint_y=None, height=dp(52))
        btn.bind(on_release=lambda *_: self.get_age())
        root.add_widget(btn)

        root.add_widget(lbl("OFFLINE AGE CALCULATOR", 9, GRAY))

        Clock.schedule_interval(self.tick, 1)
        self.tick()
        return root

    def error(self):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        content.add_widget(Label(text="Please enter a valid Jalali birth date.",
                                 halign="center"))
        close = Button(text="OK", size_hint_y=None, height=dp(44))
        content.add_widget(close)
        pop = Popup(title="Invalid Date", content=content,
                    size_hint=(0.85, 0.35))
        close.bind(on_release=pop.dismiss)
        pop.open()

    def get_age(self):
        try:
            y, m, d = [int(e.text) for e in self.entries]
            bd = jdatetime.date(y, m, d)
            if bd > jdatetime.date.today():
                raise ValueError
            self.birth_date = bd
            self.update_age()
        except Exception:
            self.error()

    def update_age(self):
        bd = self.birth_date
        if bd is None:
            return
        now = datetime.now()
        today = jdatetime.date.fromgregorian(date=now.date())

        years = today.year - bd.year
        if (today.month, today.day) < (bd.month, bd.day):
            years -= 1

        try:
            ann = jdatetime.date(bd.year + years, bd.month, bd.day)
        except ValueError:
            ann = jdatetime.date(bd.year + years, bd.month, 29)

        start = datetime.combine(ann.togregorian(), datetime.min.time())
        elapsed = int((now - start).total_seconds())

        days = elapsed // 86400
        hours = (elapsed % 86400) // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        self.age_display.text = f"{years} YEARS"
        self.detail_display.text = (
            f"{days} Days\n{hours:02} Hours : {minutes:02} Minutes : {seconds:02} Seconds"
        )

    def tick(self, *_):
        self.clock_display.text = "PHONE TIME  |  " + datetime.now().strftime("%H:%M:%S")
        self.update_age()


if __name__ == "__main__":
    AgeApp().run()
