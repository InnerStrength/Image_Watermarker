from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from watermarker import Watermarker

HOVER = "#729fe3"
FONT = ("verdana", 12, 'normal')
ENTRY_FONT = ("verdana", 10, 'normal')
PAD = 5
BG = "#80b3ff"
water_marks = []
images_to_watermark = []
directory = ""


def insert_text(list_items, entry):
    insert = ""
    for image in list_items:
        image_split = image.split("/")[-1]
        insert += f"{image_split}, "
    entry.delete(0, END)
    entry.insert(0, insert)


def open_watermark():
    global water_marks
    water_marks = fd.askopenfilenames(filetypes=[("Image files", ".jpg .jpeg .png .bmp .gif")])
    insert_text(water_marks, watermark_input)


def select_directory():
    global directory
    directory = fd.askdirectory()
    save_directory_input.delete(0, END)
    save_directory_input.insert(0, directory)


def select_images():
    global images_to_watermark
    images_to_watermark = fd.askopenfilenames(filetypes=[("Image files", ".jpg .jpeg .png .bmp .gif")])
    insert_text(images_to_watermark, select_files_input)


def create_image():
    global images_to_watermark
    positions = position_input.get().lower().split(",")
    errors = [p for p in positions if p != "ll" and p != "lr" and p != "ur" and p != "ul"]

    if directory == "" or water_marks == [] or images_to_watermark == []:
        messagebox.showerror(title="Missing Requirements",
                             message="Please check that you have selected images, "
                                     "watermarks and a directory to save your files")
    elif len(positions) != len(water_marks):
        messagebox.showerror(title="Position Error",
                             message="Double check that each watermark has a position assigned to it")
    elif len(errors) > 0:
        messagebox.showerror(title="Invalid Position",
                             message="Double check your positions:\nMake sure you only used one of the valid two digit "
                                     "options.\n")
    else:
        for image in images_to_watermark:
            image_split = image.split("/")
            filename = image_split[-1]
            image_to_mark = Watermarker(img=image)

            for i in range(len(positions)):
                try:
                    image_to_mark.set_watermark(watermark=water_marks[i])
                    image_to_mark.watermark_image(position=positions[i])
                except IndexError:
                    pass

            image_to_mark.save_image(f"{directory}/{filename}")

        messagebox.showinfo(title="Creation Successful", message="Image Creation Successful")
        save_directory_input.delete(0, END)
        watermark_input.delete(0, END)
        position_input.delete(0, END)
        select_files_input.delete(0, END)


# -------------------------- Window Set-UP ----------------------- #
window = Tk()
window.config(padx=80, pady=30)
window.title("Watermarker")

# -------------------------- GUI Set-UP -------------------------- #
select_files_label = Label(text="Files to watermark:", font=FONT, anchor="e")
select_files_label.grid(column=1, row=1, columnspan=2, pady=PAD)

select_files_input = Entry(width=22, takefocus=1, font=ENTRY_FONT)
select_files_input.grid(column=2, row=2, pady=PAD, ipady=PAD, ipadx=4)
search_button = Button(text="Select Images", width=17, font=FONT, command=select_images,
                       activebackground=HOVER, bg=BG, highlightthickness=0)
search_button.grid(column=3, row=2, pady=PAD)

watermark_input = Entry(width=22, takefocus=1, font=ENTRY_FONT)
watermark_input.grid(column=2, row=3, pady=PAD, ipady=PAD, ipadx=4)
watermark_button = Button(text="Select Watermark", width=17, command=open_watermark,
                          font=FONT, activebackground=HOVER, bg=BG, highlightthickness=0)
watermark_button.grid(column=3, row=3, pady=PAD)

position_label = Label(text="Watermark Position:", font=FONT, anchor="e", width=20)
position_label.grid(column=4, row=3, pady=PAD)
position_input = Entry(width=22, takefocus=1, font=ENTRY_FONT)
position_input.grid(column=5, row=3, pady=PAD, ipady=PAD, ipadx=4)
position_desc_label = Label(text="Acceptable positions are LL, LR, UR, and UL"
                                 "\nwrite comma separated for each watermark", font=FONT, anchor="e")
position_desc_label.grid(column=4, row=2, pady=PAD, columnspan=2)

save_directory_input = Entry(width=22, takefocus=1, font=ENTRY_FONT)
save_directory_input.grid(column=2, row=4, pady=PAD, ipady=PAD, ipadx=4)
save_directory_button = Button(text="Select Save Directory", width=17, command=select_directory,
                               font=FONT, activebackground=HOVER, bg=BG, highlightthickness=0)
save_directory_button.grid(column=3, row=4, pady=PAD)

generate_button = Button(text="Create Images", width=41, font=FONT, command=create_image,
                         activebackground=HOVER, bg=BG, highlightthickness=0)
generate_button.grid(column=2, row=5, columnspan=4, pady=7)

window.mainloop()
