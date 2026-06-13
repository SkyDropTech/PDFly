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
        """
        if not image_paths:
            raise ValueError("No images selected.")

        images = []

        try:
            total = len(image_paths)

            for index, path in enumerate(image_paths):
                if not os.path.exists(path):
                    continue
                
                try:
                    # 1. Open the raw image
                    raw_image = Image.open(path)
                    
                    # 2. Fix rotation from smartphone cameras
                    raw_image = ImageOps.exif_transpose(raw_image)

                    # 3. Create a completely fresh, clean white RGB canvas
                    # This destroys any buggy JPEG metadata or format conflicts
                    clean_image = Image.new("RGB", raw_image.size, (255, 255, 255))

                    # 4. Paste the original image onto the clean canvas
                    if raw_image.mode in ('RGBA', 'LA') or (raw_image.mode == 'P' and 'transparency' in raw_image.info):
                        # Paste with transparency mask so backgrounds stay white, not black
                        clean_image.paste(raw_image, mask=raw_image.convert('RGBA').split()[3])
                    else:
                        # Paste standard images directly
                        clean_image.paste(raw_image)

                    images.append(clean_image)

                except Exception as e:
                    raise ValueError(f"Error processing {os.path.basename(path)}: {str(e)}")

                if progress_callback:
                    progress_callback(index + 1, total)

            if len(images) == 0:
                raise ValueError("No valid images found.")

            first = images[0]
            remaining = images[1:]

            # 5. Save explicitly as a PDF
            first.save(
                output_path,
                format="PDF",
                save_all=True,
                append_images=remaining,
                resolution=100.0
            )

            return True

        finally:
            # Clean up memory to keep the server running fast
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