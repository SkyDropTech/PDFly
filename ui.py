import os
import customtkinter as ctk

from PIL import Image, ImageTk

from tkinter import filedialog, messagebox

from converter import PDFConverter


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PDFLYApp:

    def run(self):
        self.root.mainloop()

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("PDFLY - Professional Image to PDF Converter")

        self.root.geometry("1450x850")

        self.root.minsize(1200, 700)

        self.image_paths = []

        self.preview_image = None

        self.build_ui()



    def build_ui(self):

        self.create_header()

        self.create_main()

        # self.create_statusbar()



    def create_header(self):

        self.header = ctk.CTkFrame(
            self.root,
            height=70,
            corner_radius=0
        )

        self.header.pack(
            fill="x"
        )

        self.logo = ctk.CTkLabel(
            self.header,
            text="PDFLY",
            font=("Segoe UI", 34, "bold")
        )

        self.logo.pack(
            side="left",
            padx=25
        )

        self.subtitle = ctk.CTkLabel(
            self.header,
            text="Professional Image to PDF Converter",
            font=("Segoe UI", 18)
        )

        self.subtitle.pack(
            side="left"
        )

        self.about_btn = ctk.CTkButton(
            self.header,
            text="About",
            width=100
        )

        self.about_btn.pack(
            side="right",
            padx=15
        )



    def create_main(self):

        self.main = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.create_left_panel()

        self.create_right_panel()

    def create_left_panel(self):

        self.left_panel = ctk.CTkFrame(
            self.main,
            width=380,
            corner_radius=15
        )

        self.left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        self.left_panel.pack_propagate(False)

        self.images_title = ctk.CTkLabel(
            self.left_panel,
            text="Selected Images",
            font=("Segoe UI", 24, "bold")
        )

        self.images_title.pack(
            pady=(20, 10)
        )

        self.image_list = ctk.CTkTextbox(
            self.left_panel,
            width=330,
            height=450,
            font=("Segoe UI", 15),
            corner_radius=10
        )

        self.image_list.pack(
            padx=20,
            fill="both",
            expand=True
        )

        self.image_count = ctk.CTkLabel(
            self.left_panel,
            text="Images : 0",
            font=("Segoe UI", 16)
        )

        self.image_count.pack(
            pady=(10, 5)
        )

        self.add_button = ctk.CTkButton(
            self.left_panel,
            text="📂  Add Images",
            height=45,
            font=("Segoe UI", 16, "bold"),
            command=self.add_images
        )

        self.add_button.pack(
            fill="x",
            padx=20,
            pady=(10, 8)
        )

        self.remove_button = ctk.CTkButton(
            self.left_panel,
            text="❌  Remove All",
            height=45,
            font=("Segoe UI", 16),
            fg_color="#c0392b",
            hover_color="#a93226",
            command=self.remove_all
        )

        self.remove_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.move_up_button = ctk.CTkButton(
            self.left_panel,
            text="⬆  Move Up",
            height=42,
            font=("Segoe UI", 15)
        )

        self.move_up_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.move_down_button = ctk.CTkButton(
            self.left_panel,
            text="⬇  Move Down",
            height=42,
            font=("Segoe UI", 15)
        )

        self.move_down_button.pack(
            fill="x",
            padx=20,
            pady=(8, 20)
        )



    def add_images(self):

        files = filedialog.askopenfilenames(

            title="Select Images",

            filetypes=[

                (
                    "Images",

                    "*.png *.jpg *.jpeg *.bmp *.webp"

                )

            ]

        )

        if not files:
            return

        for file in files:

            if file not in self.image_paths:

                self.image_paths.append(file)

                name = os.path.basename(file)

                self.image_list.insert("end", "🖼  " + name + "\n")

        self.image_count.configure(

            text=f"Images : {len(self.image_paths)}"

        )



    def remove_all(self):

        self.image_paths.clear()

        self.image_list.delete("1.0", "end")

        self.image_count.configure(

            text="Images : 0"

        )
    def create_right_panel(self):

        self.right_panel = ctk.CTkFrame(
            self.main,
            corner_radius=15
        )

        self.right_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==========================
        # Preview Title
        # ==========================

        self.preview_title = ctk.CTkLabel(
            self.right_panel,
            text="Image Preview",
            font=("Segoe UI", 26, "bold")
        )

        self.preview_title.pack(
            pady=(20, 10)
        )

        # ==========================
        # Preview Area
        # ==========================

        self.preview_frame = ctk.CTkFrame(
            self.right_panel,
            height=450,
            corner_radius=12,
            fg_color="#242424"
        )

        self.preview_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="🖼\n\nNo Image Selected",
            font=("Segoe UI", 22),
            justify="center"
        )

        self.preview_label.pack(
            expand=True
        )

        # ==========================
        # Information Card
        # ==========================

        self.info_frame = ctk.CTkFrame(
            self.right_panel,
            height=90,
            corner_radius=12
        )

        self.info_frame.pack(
            fill="x",
            padx=25,
            pady=(10, 0)
        )

        self.file_name_label = ctk.CTkLabel(
            self.info_frame,
            text="File : -",
            anchor="w",
            font=("Segoe UI", 15)
        )

        self.file_name_label.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.file_size_label = ctk.CTkLabel(
            self.info_frame,
            text="Size : -",
            anchor="w",
            font=("Segoe UI", 15)
        )

        self.file_size_label.pack(
            anchor="w",
            padx=15
        )

        self.resolution_label = ctk.CTkLabel(
            self.info_frame,
            text="Resolution : -",
            anchor="w",
            font=("Segoe UI", 15)
        )

        self.resolution_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        # ==========================
        # Progress
        # ==========================

        self.progress = ctk.CTkProgressBar(
            self.right_panel,
            height=18
        )

        self.progress.pack(
            fill="x",
            padx=25,
            pady=(20, 8)
        )

        self.progress.set(0)

        self.progress_text = ctk.CTkLabel(
            self.right_panel,
            text="Ready",
            font=("Segoe UI", 15)
        )

        self.progress_text.pack()

        # ==========================
        # Convert Button
        # ==========================

        self.convert_button = ctk.CTkButton(
            self.right_panel,
            text="🚀  Convert To PDF",
            height=55,
            font=("Segoe UI", 20, "bold"),
            command=self.convert_pdf
        )

        self.convert_button.pack(
            fill="x",
            padx=25,
            pady=20
        )



    def convert_pdf(self):

        if len(self.image_paths) == 0:

            messagebox.showwarning(
                "No Images",
                "Please add images first."
            )

            return

        save_path = filedialog.asksaveasfilename(

            defaultextension=".pdf",

            filetypes=[

                ("PDF File", "*.pdf")

            ]

        )

        if not save_path:
            return

        self.progress_text.configure(
            text="Converting..."
        )

        self.progress.set(0.30)

        try:

            PDFConverter.convert(
                self.image_paths,
                save_path
            )

            self.progress.set(1)

            self.progress_text.configure(
                text="Completed Successfully"
            )

            messagebox.showinfo(

                "Success",

                "PDF Created Successfully!"

            )

        except Exception as e:

            self.progress.set(0)

            self.progress_text.configure(
                text="Failed"
            )

            messagebox.showerror(

                "Error",

                str(e)

            )