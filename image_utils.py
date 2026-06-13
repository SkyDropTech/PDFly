"""
PDFLY
Configuration File
"""

import os


class Config:

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME = "PDFLY"

    VERSION = "1.0.0"

    WINDOW_TITLE = "PDFLY - Professional Image to PDF Converter"

    WINDOW_WIDTH = 1450

    WINDOW_HEIGHT = 850

    MIN_WIDTH = 1200

    MIN_HEIGHT = 700

    # ==========================================================
    # Theme
    # ==========================================================

    APPEARANCE_MODE = "dark"

    COLOR_THEME = "blue"

    PRIMARY_COLOR = "#1F6AA5"

    SUCCESS_COLOR = "#2ECC71"

    ERROR_COLOR = "#E74C3C"

    WARNING_COLOR = "#F39C12"

    BACKGROUND_COLOR = "#202124"

    CARD_COLOR = "#2B2B2B"

    # ==========================================================
    # Images
    # ==========================================================

    SUPPORTED_FORMATS = (

        ".jpg",

        ".jpeg",

        ".png",

        ".bmp",

        ".webp"

    )

    FILE_DIALOG_TYPES = [

        (

            "Images",

            "*.jpg *.jpeg *.png *.bmp *.webp"

        )

    ]

    PREVIEW_SIZE = (

        700,

        500

    )

    THUMBNAIL_SIZE = (

        120,

        120

    )

    # ==========================================================
    # PDF
    # ==========================================================

    DEFAULT_OUTPUT_NAME = "output.pdf"

    PDF_RESOLUTION = 100

    # ==========================================================
    # Paths
    # ==========================================================

    ROOT_PATH = os.path.dirname(

        os.path.abspath(__file__)

    )

    ASSETS_PATH = os.path.join(

        ROOT_PATH,

        "assets"

    )

    OUTPUT_PATH = os.path.join(

        ROOT_PATH,

        "output"

    )

    # ==========================================================
    # Assets
    # ==========================================================

    ICON_PATH = os.path.join(

        ASSETS_PATH,

        "icon.ico"

    )

    LOGO_PATH = os.path.join(

        ASSETS_PATH,

        "logo.png"

    )

    EMPTY_IMAGE = os.path.join(

        ASSETS_PATH,

        "empty.png"

    )

    ADD_ICON = os.path.join(

        ASSETS_PATH,

        "add.png"

    )

    REMOVE_ICON = os.path.join(

        ASSETS_PATH,

        "remove.png"

    )

    UP_ICON = os.path.join(

        ASSETS_PATH,

        "up.png"

    )

    DOWN_ICON = os.path.join(

        ASSETS_PATH,

        "down.png"

    )

    PDF_ICON = os.path.join(

        ASSETS_PATH,

        "pdf.png"

    )

    ABOUT_ICON = os.path.join(

        ASSETS_PATH,

        "about.png"

    )

    # ==========================================================
    # Messages
    # ==========================================================

    READY_MESSAGE = "Ready"

    NO_IMAGE_MESSAGE = "No Image Selected"

    SUCCESS_MESSAGE = "PDF Created Successfully"

    ERROR_MESSAGE = "Something went wrong"

    # ==========================================================
    # Utility
    # ==========================================================

    @classmethod
    def create_folders(cls):

        os.makedirs(

            cls.OUTPUT_PATH,

            exist_ok=True

        )