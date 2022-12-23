from display import Colors, for_lcd
from ir_remote import Keys


class Menu:
    MARGIN_TOP = 8
    MARGIN_LEFT = 10
    LINE_SPACING = 10

    LINES = 12

    def __init__(self, lcd, ir):
        self.lcd = lcd
        self.ir = ir
        self.page = None

        self.entered_code = ""

    def set_menu_page(self, page):
        self.page = page

    def process(self):
        if not self.ir.key_available():
            return
        code = self.ir.get_key()
        if Keys.is_number(code):
            self.entered_code += str(Keys.NUMBER_KEYS.index(code))
        if len(self.entered_code)==2:
            selection = int(self.entered_code)
            self.entered_code = ""
            if selection>=1 and selection<=len(self.page.entries):
                return self.page.entries[selection-1]["cb"]()

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
        self.page.draw(self.lcd)
        self.lcd.show()
