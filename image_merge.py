from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os
import platform


class ImageMerge:
    def __init__(self):
        self.image_background = None
        self.image_foreground = None
        self.folder = None
        self.height = None
        self.width = None
        self.b = None
        self.frame = Frame(root, height=20, relief=SUNKEN)
        self.frame.grid(row=5, columnspan=10, sticky="w")
        l = Label(self.frame, text='Ready', fg='black')
        l.pack(fill=X, padx=5)

    def open_folder(self):
        if platform.system() == 'Windows':
            os.startfile(self.folder)
        elif platform.system() == 'Linux':
            os.system('xdg-open "%s"' % self.folder)
        elif platform.system() == "Darwin":
            os.system('open "%s"' % self.folder)
        else:
            messagebox.showwarning("Warning", "your os is not supported")

    def get_image_background(self):
        self.image_background = None
        image = filedialog.askopenfilename(initialdir=os.path.expanduser('~'))
        if image:
            self.image_background = image
        else:
            if self.b:
                self.b.destroy()

    def get_image_foreground(self):
        self.image_foreground = None
        image = filedialog.askopenfilename(initialdir=os.path.expanduser('~'))
        if image:
            self.image_foreground = image
        else:
            if self.b:
                self.b.destroy()

    def get_folder(self):
        self.folder = None
        folder = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
        if folder:
            self.folder = folder
        else:
            if self.b:
                self.b.destroy()

    def fail(self):
        self.frame.destroy()
        self.frame = Frame(root, height=25, relief=SUNKEN)
        self.frame.grid(row=5, columnspan=10, sticky="w")
        l = Label(self.frame, text='Failed!!!', fg='red')
        l.pack(fill=X, padx=5)

    def edit_image(self):
        try:
            self.height = int(height_entry.get())
            self.width = int(width_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please Supply Numbers for Height and Width")
            self.fail()

        if not self.image_background or not self.image_foreground:
            messagebox.showerror("Error", "Please select images for edit")
            self.fail()

        elif not self.height or not self.width:
            messagebox.showerror("Error", "Please specify Height and Width for the new Image")
            self.fail()

        else:
            self.frame.destroy()
            self.frame = Frame(root, height=25, relief=SUNKEN)
            self.frame.grid(row=5, columnspan=10, sticky="w")
            self.get_folder()
            if self.folder:
                try:
                    size = self.height, self.width
                    background = Image.open(self.image_background)
                    background = background.resize(size, Image.ANTIALIAS)
                    foreground = Image.open(self.image_foreground)
                    foreground = foreground.resize(size, Image.ANTIALIAS)
                    new_image = os.path.join(self.folder, 'out.jpg')
                    Image.blend(background, foreground, .7).save(new_image)
                    self.frame.destroy()
                    self.frame = Frame(root, height=25, relief=SUNKEN)
                    self.frame.grid(row=5, columnspan=10, sticky="w")
                    l = Label(self.frame, text='Sucess!!!', fg='green')
                    l.pack(fill=X, padx=5)
                    self.b = Button(root, text='Open Folder', command=self.open_folder)
                    self.b.grid(row=4, column=0, columnspan=5)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    self.fail()


if __name__ == '__main__':
    root = Tk()
    root.title('Image Editor')
    root.grid_columnconfigure(2, weight=2)
    root.grid_rowconfigure(2, weight=2)
    menu = Menu(root)
    file_menu = Menu(menu, tearoff=0)
    about_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='About', menu=about_menu)
    root.config(menu=menu)
    my_app = ImageMerge()
    root.geometry("400x140")

    def display_about(event=None):
        messagebox.showinfo("About",
                            "Created by Tony Jafar")


    def exit_app(event=None):
        if messagebox.askokcancel("Quit?", "Really quit?"):
            root.destroy()

    def select_back_image(event=None):
            my_app.get_image_background()
            return 'break'

    def select_fore_image(event=None):
            my_app.get_image_foreground()
            return 'break'

    def start(event=None):
            my_app.edit_image()
            return 'break'

    def select_all_e1(event=None):
        height_entry.select_range(0, END)
        return "break"


    def select_all_e2(event=None):
        width_entry.select_range(0, END)
        return "break"


    Label(root, text='Enter Height', fg='blue').grid(row=0, column=0)
    height_entry = Entry(root)
    height_entry.grid(row=0, column=1)
    Label(root, text='Enter Width', fg='blue').grid(row=0, column=3)
    height_entry.focus()
    width_entry = Entry(root)
    width_entry.grid(row=0, column=4)
    Button(root, text='Add Background Image', command=select_back_image
           ).grid(row=2, column=0, columnspan=5,sticky="w")
    Button(root, text='Add Foreground Image', command=select_fore_image
           ).grid(row=2, column=1, columnspan=5, sticky="e")
    Button(root, text='   Start   ', command=start
           ).grid(row=3, column=0, columnspan=5)
    about_menu.add_command(label='About', command=display_about)
    root.protocol('WM_DELETE_WINDOW', exit_app)
    height_entry.bind('<Control-A>', select_all_e1)
    height_entry.bind('<Control-a>', select_all_e1)
    width_entry.bind('<Control-A>', select_all_e2)
    width_entry.bind('<Control-a>', select_all_e2)
    root.mainloop()

