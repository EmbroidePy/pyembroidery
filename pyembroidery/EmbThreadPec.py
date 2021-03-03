from .EmbThread import EmbThread


def get_thread_set():
    return [
        None,  #  EmbThreadPec(0, 0, 0, "Unknown", "0"),
        EmbThreadPec(14, 31, 124, "Prussian Blue", "1"),
        EmbThreadPec(10, 85, 163, "Blue", "2"),
        EmbThreadPec(0, 135, 119, "Teal Green", "3"),
        EmbThreadPec(75, 107, 175, "Cornflower Blue", "4"),
        EmbThreadPec(237, 23, 31, "Red", "5"),
        EmbThreadPec(209, 92, 0, "Reddish Brown", "6"),
        EmbThreadPec(145, 54, 151, "Magenta", "7"),
        EmbThreadPec(228, 154, 203, "Light Lilac", "8"),
        EmbThreadPec(145, 95, 172, "Lilac", "9"),
        EmbThreadPec(158, 214, 125, "Mint Green", "10"),
        EmbThreadPec(232, 169, 0, "Deep Gold", "11"),
        EmbThreadPec(254, 186, 53, "Orange", "12"),
        EmbThreadPec(255, 255, 0, "Yellow", "13"),
        EmbThreadPec(112, 188, 31, "Lime Green", "14"),
        EmbThreadPec(186, 152, 0, "Brass", "15"),
        EmbThreadPec(168, 168, 168, "Silver", "16"),
        EmbThreadPec(125, 111, 0, "Russet Brown", "17"),
        EmbThreadPec(255, 255, 179, "Cream Brown", "18"),
        EmbThreadPec(79, 85, 86, "Pewter", "19"),
        EmbThreadPec(0, 0, 0, "Black", "20"),
        EmbThreadPec(11, 61, 145, "Ultramarine", "21"),
        EmbThreadPec(119, 1, 118, "Royal Purple", "22"),
        EmbThreadPec(41, 49, 51, "Dark Gray", "23"),
        EmbThreadPec(42, 19, 1, "Dark Brown", "24"),
        EmbThreadPec(246, 74, 138, "Deep Rose", "25"),
        EmbThreadPec(178, 118, 36, "Light Brown", "26"),
        EmbThreadPec(252, 187, 197, "Salmon Pink", "27"),
        EmbThreadPec(254, 55, 15, "Vermillion", "28"),
        EmbThreadPec(240, 240, 240, "White", "29"),
        EmbThreadPec(106, 28, 138, "Violet", "30"),
        EmbThreadPec(168, 221, 196, "Seacrest", "31"),
        EmbThreadPec(37, 132, 187, "Sky Blue", "32"),
        EmbThreadPec(254, 179, 67, "Pumpkin", "33"),
        EmbThreadPec(255, 243, 107, "Cream Yellow", "34"),
        EmbThreadPec(208, 166, 96, "Khaki", "35"),
        EmbThreadPec(209, 84, 0, "Clay Brown", "36"),
        EmbThreadPec(102, 186, 73, "Leaf Green", "37"),
        EmbThreadPec(19, 74, 70, "Peacock Blue", "38"),
        EmbThreadPec(135, 135, 135, "Gray", "39"),
        EmbThreadPec(216, 204, 198, "Warm Gray", "40"),
        EmbThreadPec(67, 86, 7, "Dark Olive", "41"),
        EmbThreadPec(253, 217, 222, "Flesh Pink", "42"),
        EmbThreadPec(249, 147, 188, "Pink", "43"),
        EmbThreadPec(0, 56, 34, "Deep Green", "44"),
        EmbThreadPec(178, 175, 212, "Lavender", "45"),
        EmbThreadPec(104, 106, 176, "Wisteria Violet", "46"),
        EmbThreadPec(239, 227, 185, "Beige", "47"),
        EmbThreadPec(247, 56, 102, "Carmine", "48"),
        EmbThreadPec(181, 75, 100, "Amber Red", "49"),
        EmbThreadPec(19, 43, 26, "Olive Green", "50"),
        EmbThreadPec(199, 1, 86, "Dark Fuschia", "51"),
        EmbThreadPec(254, 158, 50, "Tangerine", "52"),
        EmbThreadPec(168, 222, 235, "Light Blue", "53"),
        EmbThreadPec(0, 103, 62, "Emerald Green", "54"),
        EmbThreadPec(78, 41, 144, "Purple", "55"),
        EmbThreadPec(47, 126, 32, "Moss Green", "56"),
        EmbThreadPec(255, 204, 204, "Flesh Pink", "57"),
        EmbThreadPec(255, 217, 17, "Harvest Gold", "58"),
        EmbThreadPec(9, 91, 166, "Electric Blue", "59"),
        EmbThreadPec(240, 249, 112, "Lemon Yellow", "60"),
        EmbThreadPec(227, 243, 91, "Fresh Green", "61"),
        EmbThreadPec(255, 153, 0, "Orange", "62"),
        EmbThreadPec(255, 240, 141, "Cream Yellow", "63"),
        EmbThreadPec(255, 200, 200, "Applique", "64"),
    ]


class EmbThreadPec(EmbThread):
    def __init__(self, red, green, blue, description, catalog_number):
        EmbThread.__init__(self)
        self.set_color(red, green, blue)
        self.description = description
        self.catalog_number = catalog_number
        self.brand = "Brother"
        self.chart = "Brother"
