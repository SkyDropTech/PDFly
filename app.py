"""
PDFLY
Professional Image to PDF Converter

Author : Rishikesh Shedge
Version: 1.0.0
"""

from tkinter import messagebox
import traceback

from ui import PDFLYApp


def main():
    """
    Application Entry Point
    """
    app = PDFLYApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        messagebox.showerror(
            "Unexpected Error",
            f"Something went wrong.\n\n{error}"
        )

        with open("error.log", "a", encoding="utf-8") as file:
            file.write("\n" + "=" * 80 + "\n")
            file.write(traceback.format_exc())