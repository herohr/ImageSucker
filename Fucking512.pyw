import tkinter
from tkinter import messagebox
from PIL import Image
import os
import threading


class GUI:
    def __init__(self):
        """初始化图形界面"""
        self.tk = tkinter.Tk(className="Ralee Studio 图片格式转换工具")

        self.file_box = None
        self.make_file_box()
        self.make_two_entry()
        self.make_save_button()
        self.make_lot_size_button()
        self.tk.mainloop()

    def make_file_box(self):
        self.file_box = tkinter.Listbox(width=30, height=20)
        for i in list_files():
            self.file_box.insert(0, i)
        self.file_box.grid(row=0, column=0, rowspan=12)

    def make_two_entry(self):
        self.size_label = tkinter.Label(text="尺寸")
        self.size_entry_1 = tkinter.Entry(width=10)
        self.size_entry_2 = tkinter.Entry(width=10)
        self.size_label.grid(row=0, column=1, columnspan=2)
        self.size_entry_1.grid(row=1, column=1)
        self.size_entry_2.grid(row=1, column=2)

        self.form_label = tkinter.Label(text='格式')
        self.form_entry = tkinter.Entry(width=20)
        self.form_label.grid(row=2, column=1, columnspan=2)
        self.form_entry.grid(row=3, column=1, columnspan=2)

        self.rename_label = tkinter.Label(text='重命名为:')
        self.rename_entry = tkinter.Entry(width=20)
        self.rename_label.grid(row=4, column=1, columnspan=2)
        self.rename_entry.grid(row=5, column=1, columnspan=2)

    def make_save_button(self):
        self.save_size_label = tkinter.Label(text="预计大小: 未知")
        self.save_button = tkinter.Button(text="保存", command=self.format)
        self.save_button.grid(row=6, column=1, columnspan=2)
        self.save_size_label.grid(row=7, column=1, columnspan=2)

    def make_resize_function(self, size):
        """为resize_button绑定回调"""
        def resize():
            filename = self.file_box.get(self.file_box.curselection()[0])
            self.format(filename, '{}x{}'.format(size, size), (size, size), 'jpeg')

        return resize

    def make_lot_size_button(self):
        sizes = [512, 256, 128, 64, 32, 16]

        for (index, size) in enumerate(sizes):
            button = tkinter.Button(text='{}*{}'.format(size, size),
                                    width=10,
                                    command=self.make_resize_function(size))

            button.grid(row=8 + index // 2, column=1 + index % 2)

    def selected_form(self):
        try:
            filename = self.file_box.get(self.file_box.curselection()[0])
            if filename:
                width = int(self.size_entry_1.get())
                height = int(self.size_entry_2.get())
                if width and height:
                    form = self.form_entry.get()
                    form = form if form else 'jpeg'
                    rename = self.rename_entry.get()
                    return format(filename, rename, (width, height), form)
                else:
                    show_info("好像没输入尺寸？")
        except IndexError:
            show_info('好像没选中文件？')

    def format(self, filename, rename, size=(), form='jpeg'):
        """有关图形界面的一个format函数，实际的转换函数为异步执行"""
        def do_format():
            try:
                file_size = format_img("./" + filename, rename, size, form)
            except Exception as e:
                show_info(e)
            else:
                messagebox.showinfo('转换完成', '文件大小: {:.2f} KB'.format(file_size / 1024))

        threading.Thread(target=do_format).start()  # 异步执行


def show_info(msg):
    messagebox.showinfo("出了一点小状况!", msg)


def list_files():
    a = os.listdir(os.getcwd())
    return [file for file in a if os.path.isfile('./' + file)]  # 一个当前目录文件的列表


def format_img(img_path, img_name="unnaming", img_size=(), img_form='jpeg'):
    with Image.open(img_path) as image:
        img_form = "jpeg" if img_form.lower() == "jpg" else img_form  # 将"jpg" 变为 "jpeg"
        output = image.resize(img_size, Image.ANTIALIAS)  # Image.ANTIALIAS 在这里可以增强画质

        img_name = img_name + '.' + img_form if not img_name.split('.')[-1] == img_form else img_name  # 防止多个后缀名...
        output.save(img_name, img_form)
        return os.path.getsize("./{}".format(img_name))  # 文件大小


if __name__ == "__main__":
    GUI()
