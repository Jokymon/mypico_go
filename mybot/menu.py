from display import Colors, for_lcd
from ir_remote import Keys


def callback1():
    print("Entry chosen")


class MenuPage:
    entries = [
        { "text": "Menu Entry Top", "cb": callback1 },
        { "text": "Another entry", "cb": lambda: None },
        { "text": "More Entries", "cb": lambda: None },
        { "text": "Menu Entry Bottom", "cb": lambda: None }
    ]


class Menu:
    MARGIN_TOP = 8
    MARGIN_LEFT = 10
    LINE_SPACING = 10

    LINES = 12

    def __init__(self, lcd, ir, page):
        self.lcd = lcd
        self.ir = ir
        self.page = page

        self.entered_code = ""

    def process(self):
        if not self.ir.key_available():
            return
        code = self.ir.get_key()
        if Keys.is_number(code):
            self.entered_code += str(Keys.NUMBER_KEYS.index(code))

    def draw(self):
        self.lcd.fill(for_lcd(*Colors.BLACK))
        for index, entry in enumerate(self.page.entries):
            self.lcd.text(f"{index+1:02} {entry['text']}", 
                    Menu.MARGIN_LEFT, Menu.MARGIN_TOP + index*Menu.LINE_SPACING,
                    for_lcd(*Colors.BLUE))
        self.lcd.text("Choose: ",
                    100, Menu.MARGIN_TOP + 10*Menu.LINE_SPACING,
                    for_lcd(*Colors.GREEN))
        self.lcd.text(self.entered_code+"_",
                    180, Menu.MARGIN_TOP + 10*Menu.LINE_SPACING,
                    for_lcd(*Colors.RED))
        self.lcd.show()
