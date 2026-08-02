from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Thiết lập kích thước chuẩn điện thoại
Window.clearcolor = (0, 0, 0, 1)

class RoundButton(Button):
    def __init__(self, bg_color=(0.2, 0.2, 0.2, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            r = min(self.width, self.height) / 2
            RoundedRectangle(pos=self.pos, size=self.size, radius=[r])

class CalculatorApp(App):
    def build(self):
        self.expression = ""
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Màn hình hiển thị
        self.sub_display = Label(text="", font_size=20, halign='right', size_hint=(1, 0.1), color=(0.6, 0.6, 0.6, 1))
        self.sub_display.bind(size=self.sub_display.setter('text_size'))
        self.display = Label(text="0", font_size=48, bold=True, halign='right', size_hint=(1, 0.25), color=(1, 1, 1, 1))
        self.display.bind(size=self.display.setter('text_size'))

        self.main_layout.add_widget(self.sub_display)
        self.main_layout.add_widget(self.display)

        # Bàn phím nút tròn
        grid = GridLayout(cols=4, spacing=10, size_hint=(1, 0.65))
        
        keys = [
            ("C", (0.6, 0.6, 0.6, 1), (0, 0, 0, 1)),
            ("+/-", (0.6, 0.6, 0.6, 1), (0, 0, 0, 1)),
            ("%", (0.6, 0.6, 0.6, 1), (0, 0, 0, 1)),
            ("÷", (1, 0.6, 0, 1), (1, 1, 1, 1)),
            ("7", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("8", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("9", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("×", (1, 0.6, 0, 1), (1, 1, 1, 1)),
            ("4", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("5", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("6", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("-", (1, 0.6, 0, 1), (1, 1, 1, 1)),
            ("1", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("2", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("3", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("+", (1, 0.6, 0, 1), (1, 1, 1, 1)),
            ("0", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            (".", (0.17, 0.17, 0.18, 1), (1, 1, 1, 1)),
            ("⌫", (0.22, 0.22, 0.23, 1), (1, 0.27, 0.22, 1)),
            ("=", (1, 0.6, 0, 1), (1, 1, 1, 1))
        ]

        for text, bg, fg in keys:
            btn = RoundButton(text=text, font_size=28, bold=True, bg_color=bg, color=fg)
            btn.bind(on_press=self.on_button_click)
            grid.add_widget(btn)

        self.main_layout.add_widget(grid)
        return self.main_layout

    def on_button_click(self, instance):
        char = instance.text
        if char == "C":
            self.expression = ""
            self.display.text = "0"
            self.sub_display.text = ""
        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.display.text = self.expression if self.expression else "0"
        elif char == "=":
            try:
                expr_eval = self.expression.replace('×', '*').replace('÷', '/')
                res = round(eval(expr_eval), 8)
                self.sub_display.text = self.expression + " ="
                self.display.text = str(int(res) if isinstance(res, float) and res.is_integer() else res)
                self.expression = self.display.text
            except Exception:
                self.display.text = "Lỗi"
                self.expression = ""
        elif char == "+/-":
            if self.expression:
                self.expression = self.expression[1:] if self.expression.startswith("-") else "-" + self.expression
                self.display.text = self.expression
        elif char == "%":
            try:
                self.expression = str(float(eval(self.expression)) / 100)
                self.display.text = self.expression
            except Exception:
                pass
        else:
            if self.expression in ["0", "Lỗi"]:
                self.expression = char
            else:
                self.expression += char
            self.display.text = self.expression

if __name__ == "__main__":
    CalculatorApp().run()
      
