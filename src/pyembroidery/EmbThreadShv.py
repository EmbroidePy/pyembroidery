from .EmbThread import EmbThread


def get_thread_set():
    return [
        EmbThreadShv(0, 0, 0, "Black", "0"),
        EmbThreadShv(0, 0, 255, "Blue", "1"),
        EmbThreadShv(51, 204, 102, "Green", "2"),
        EmbThreadShv(255, 0, 0, "Red", "3"),
        EmbThreadShv(255, 0, 255, "Purple", "4"),
        EmbThreadShv(255, 255, 0, "Yellow", "5"),
        EmbThreadShv(127, 127, 127, "Gray", "6"),
        EmbThreadShv(51, 154, 255, "Light Blue", "7"),
        EmbThreadShv(0, 255, 0, "Light Green", "8"),
        EmbThreadShv(255, 127, 0, "Orange", "9"),
        EmbThreadShv(255, 160, 180, "Pink", "10"),
        EmbThreadShv(153, 75, 0, "Brown", "11"),
        EmbThreadShv(255, 255, 255, "White", "12"),
        EmbThreadShv(0, 0, 0, "Black", "13"),
        EmbThreadShv(0, 0, 0, "Black", "14"),
        EmbThreadShv(0, 0, 0, "Black", "15"),
        EmbThreadShv(0, 0, 0, "Black", "16"),
        EmbThreadShv(0, 0, 0, "Black", "17"),
        EmbThreadShv(0, 0, 0, "Black", "18"),
        EmbThreadShv(255, 127, 127, "Light Red", "19"),
        EmbThreadShv(255, 127, 255, "Light Purple", "20"),
        EmbThreadShv(255, 255, 153, "Light Yellow", "21"),
        EmbThreadShv(192, 192, 192, "Light Gray", "22"),
        EmbThreadShv(0, 0, 0, "Black", "23"),
        EmbThreadShv(0, 0, 0, "Black", "24"),
        EmbThreadShv(255, 165, 65, "Light Orange", "25"),
        EmbThreadShv(255, 204, 204, "Light Pink", "26"),
        EmbThreadShv(175, 90, 10, "Light Brown", "27"),
        EmbThreadShv(0, 0, 0, "Black", "28"),
        EmbThreadShv(0, 0, 0, "Black", "29"),
        EmbThreadShv(0, 0, 0, "Black", "30"),
        EmbThreadShv(0, 0, 0, "Black", "31"),
        EmbThreadShv(0, 0, 0, "Black", "32"),
        EmbThreadShv(0, 0, 127, "Dark Blue", "33"),
        EmbThreadShv(0, 127, 0, "Dark Green", "34"),
        EmbThreadShv(127, 0, 0, "Dark Red", "35"),
        EmbThreadShv(127, 0, 127, "Dark Purple", "36"),
        EmbThreadShv(200, 200, 0, "Dark Yellow", "37"),
        EmbThreadShv(60, 60, 60, "Dark Gray", "38"),
        EmbThreadShv(0, 0, 0, "Black", "39"),
        EmbThreadShv(0, 0, 0, "Black", "40"),
        EmbThreadShv(232, 63, 0, "Dark Orange", "41"),
        EmbThreadShv(255, 102, 122, "Dark Pink", "42"),
    ]


class EmbThreadShv(EmbThread):
    def __init__(self, red, green, blue, description, catalog_number):
        EmbThread.__init__(self)
        self.set_color(red, green, blue)
        self.description = description
        self.catalog_number = catalog_number
        self.brand = "Shv"
        self.chart = "Shv"
