"""
PDFLY
Professional Image to PDF Converter (Cloud Optimized)
"""

import os
from PIL import Image, ImageOps

class PDFConverter:
    # Cloud-Optimized A4 size at 100 DPI (Saves Memory & Prevents Vercel Timeouts)
    A4_WIDTH = 827
    A4_HEIGHT = 1169

    @staticmethod
    def convert(image_paths, output_path, progress_callback=None):
        if not image_paths:
            raise ValueError("No images selected.")

        images = []

        try:
            total = len(image_paths)

            for index, path in enumerate(image_paths):
                if not os.path.exists(path):
                    continue
                
                try:
                    # 1. Open and fix rotation
                    raw_image = Image.open(path)
                    raw_image = ImageOps.exif_transpose(raw_image)

                    # 2. Clean transparency
                    if raw_image.mode in ('RGBA', 'LA') or (raw_image.mode == 'P' and 'transparency' in raw_image.info):
                        clean_bg = Image.new("RGB", raw_image.size, (255, 255, 255))
                        clean_bg.paste(raw_image, mask=raw_image.convert('RGBA').split()[3])
                        raw_image = clean_bg
                    else:
                        raw_image = raw_image.convert("RGB")

                    # 3. Calculate "Perfect Fit" Ratio
                    img_w, img_h = raw_image.size
                    ratio = min(PDFConverter.A4_WIDTH / img_w, PDFConverter.A4_HEIGHT / img_h)
                    
                    new_w = int(img_w * ratio)
                    new_h = int(img_h * ratio)

                    # 4. Resize (Using BILINEAR instead of LANCZOS for 5x faster cloud processing)
                    raw_image = raw_image.resize((new_w, new_h), Image.Resampling.BILINEAR)

                    # 5. Create a blank white A4 canvas
                    a4_canvas = Image.new("RGB", (PDFConverter.A4_WIDTH, PDFConverter.A4_HEIGHT), (255, 255, 255))

                    # 6. Paste perfectly centered
                    x_offset = (PDFConverter.A4_WIDTH - new_w) // 2
                    y_offset = (PDFConverter.A4_HEIGHT - new_h) // 2
                    a4_canvas.paste(raw_image, (x_offset, y_offset))

                    images.append(a4_canvas)

                except Exception as e:
                    raise ValueError(f"Error processing {os.path.basename(path)}: {str(e)}")

                if progress_callback:
                    progress_callback(index + 1, total)

            if len(images) == 0:
                raise ValueError("No valid images found.")

            # 7. Save explicitly as a PDF
            first = images[0]
            remaining = images[1:]
            first.save(
                output_path,
                format="PDF",
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
    def get_pdf_size(file_path):
        if not os.path.exists(file_path): return "0 KB"
        size = os.path.getsize(file_path)
        if size < 1024: return f"{size} Bytes"
        if size < 1024 * 1024: return f"{size / 1024:.2f} KB"
        return f"{size / (1024 * 1024):.2f} MB"