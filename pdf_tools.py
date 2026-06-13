"""
PDFLY
Professional Image to PDF Converter
"""

import os

from PIL import Image, ImageOps


class PDFConverter:

    @staticmethod
    def convert(
        image_paths,
        output_path,
        progress_callback=None
    ):
        """
        Convert multiple images into a single PDF.

        Parameters
        ----------
        image_paths : list[str]
        output_path : str
        progress_callback : function(current, total)
        """

        if not image_paths:
            raise ValueError("No images selected.")

        images = []

        try:

            total = len(image_paths)

            for index, path in enumerate(image_paths):

                if not os.path.exists(path):
                    continue

                image = Image.open(path)

                # Fix EXIF orientation
                image = ImageOps.exif_transpose(image)

                # Convert every image to RGB
                if image.mode != "RGB":
                    image = image.convert("RGB")

                images.append(image)

                if progress_callback:

                    progress_callback(

                        index + 1,

                        total

                    )

            if len(images) == 0:

                raise ValueError(

                    "No valid images found."

                )

            first = images[0]

            remaining = images[1:]

            first.save(

                output_path,

                save_all=True,

                append_images=remaining,

                resolution=100.0

            )

            return True

        finally:

            for image in images:

                try:

                    image.close()

                except Exception:

                    pass

    @staticmethod
    def validate_output(output_path):

        if not output_path:

            return False

        folder = os.path.dirname(output_path)

        return os.path.exists(folder)

    @staticmethod
    def supported_formats():

        return (

            ".jpg",

            ".jpeg",

            ".png",

            ".bmp",

            ".webp"

        )

    @staticmethod
    def get_pdf_size(file_path):

        if not os.path.exists(file_path):

            return "0 KB"

        size = os.path.getsize(file_path)

        if size < 1024:

            return f"{size} Bytes"

        if size < 1024 * 1024:

            return f"{size / 1024:.2f} KB"

        return f"{size / (1024 * 1024):.2f} MB"

    @staticmethod
    def image_count(image_paths):

        return len(image_paths)

    @staticmethod
    def output_exists(output_path):

        return os.path.exists(output_path)