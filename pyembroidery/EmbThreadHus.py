from .EmbThread import EmbThread


def get_thread_set():
    return [
        EmbThreadHus("#000000", "Black", "026"),
        EmbThreadHus("#0000e7", "Blue", "005"),
        EmbThreadHus("#00c600", "Green", "002"),
        EmbThreadHus("#ff0000", "Red", "014"),
        EmbThreadHus("#840084", "Purple", "008"),
        EmbThreadHus("#ffff00", "Yellow", "020"),
        EmbThreadHus("#848484", "Grey", "024"),
        EmbThreadHus("#8484e7", "Light Blue", "006"),
        EmbThreadHus("#00ff84", "Light Green", "003"),
        EmbThreadHus("#ff7b31", "Orange", "017"),
        EmbThreadHus("#ff8ca5", "Pink", "011"),
        EmbThreadHus("#845200", "Brown", "028"),
        EmbThreadHus("#ffffff", "White", "022"),
        EmbThreadHus("#000084", "Dark Blue", "004"),
        EmbThreadHus("#008400", "Dark Green", "001"),
        EmbThreadHus("#7b0000", "Dark Red", "013"),
        EmbThreadHus("#ff6384", "Light Red", "015"),
        EmbThreadHus("#522952", "Dark Purple", "007"),
        EmbThreadHus("#ff00ff", "Light Purple", "009"),
        EmbThreadHus("#ffde00", "Dark Yellow", "019"),
        EmbThreadHus("#ffff9c", "Light Yellow", "021"),
        EmbThreadHus("#525252", "Dark Grey", "025"),
        EmbThreadHus("#d6d6d6", "Light Grey", "023"),
        EmbThreadHus("#ff5208", "Dark Orange", "016"),
        EmbThreadHus("#ff9c5a", "Light Orange", "018"),
        EmbThreadHus("#ff52b5", "Dark Pink", "010"),
        EmbThreadHus("#ffc6de", "Light Pink", "012"),
        EmbThreadHus("#523100", "Dark Brown", "027"),
        EmbThreadHus("#b5a584", "Light Brown", "029")
    ]


class EmbThreadHus(EmbThread):
    def __init__(self, color, description, catalog_number=None):
        EmbThread.__init__(self)
        self.set(color)
        self.description = description
        self.catalog_number = catalog_number
        self.brand = "Hus"
        self.chart = "Hus"

