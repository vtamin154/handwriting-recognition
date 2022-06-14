from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from numpy import imag
from preprocess import *
import cv2


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Handwriting recognition")
        self.minsize(800, 600)
        self.labelFrame = LabelFrame(text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        self.openFileBtn()
        self.rgbToBinBtn()
        # self.thinImgBtn()
        self.cropImgBtn()
        self.resizeImgBtn()
        self.exitBtn()

    def openFileBtn(self):
        self.btn_open_file = Button(
            self.labelFrame, text="Browse A File", command=self.fileDialog, width=30)
        self.btn_open_file.grid(column=1, row=1)

    def exitBtn(self):
        self.btn_exit = Button(
            self.labelFrame, text="Exit", command=exit, width=30)
        self.btn_exit.grid(column=1, row=6)

    def rgbToBinBtn(self):

        # convert rgb img to binary img
        self.btn_process = Button(
            self.labelFrame, text="Convert to Binary", command=self.binaryImg, width=30)
        self.btn_process.grid(column=1, row=2)

    def binaryImg(self):
        pre_process_img = PreProcess(self.filename)
        pre_process_img.binaryImage()

        self.type_img = Label(self, text="Binary Image")
        self.type_img.grid(column=1, row=3)

        img = Image.open('binary.png')
        photo = ImageTk.PhotoImage(img)

        self.label_img_bin = Label(self, image=photo)
        self.label_img_bin.image = photo
        self.label_img_bin.grid(column=1, row=4)

    def thinImgBtn(self):
        self.btn_thin = Button(
            self.labelFrame, text="Thinning img", command=self.thinningImg, width=30)
        self.btn_thin.grid(column=1, row=3)

    def thinningImg(self):
        pre_process_img = PreProcess('binary.png')
        pre_process_img.thinningImg()

        self.type_img = Label(self, text="Thinning Image")
        self.type_img.grid(column=2, row=3)

        thin_img = Image.open('thinning.png')
        photo = ImageTk.PhotoImage(thin_img)
        self.label_img_thin = Label(self, image=photo)
        self.label_img_thin.image = photo
        self.label_img_thin.grid(column=2, row=4)

    def cropImgBtn(self):
        self.btn_crop = Button(
            self.labelFrame, text="Crop Image", command=self.croppingImg, width=30)
        self.btn_crop.grid(column=1, row=4)

    def croppingImg(self):
        pre_process_img = PreProcess('binary.png')
        pre_process_img.cropImg()
        self.type_img = Label(self, text="Cropping Image")
        self.type_img.grid(column=3, row=3, padx=40)

        crop_image = Image.open('crop_img.png')
        photo = ImageTk.PhotoImage(crop_image)
        self.label_img_crop = Label(self, image=photo, padx=40)
        self.label_img_crop.image = photo
        self.label_img_crop.grid(column=3, row=4)

    def resizeImgBtn(self):
        self.btn_crop = Button(
            self.labelFrame, text="Resize Image", command=self.resizingImg, width=30)
        self.btn_crop.grid(column=1, row=5)

    def resizingImg(self):
        pre_process_img = PreProcess('binary.png')
        pre_process_img.resizeImg()
        self.type_img = Label(self, text="Resize", padx=40)
        self.type_img.grid(column=5, row=3)

        resize_img = Image.open('resize_img.png')
        photo = ImageTk.PhotoImage(resize_img)
        self.label_img_resize = Label(self, image=photo, padx=40)
        self.label_img_resize.image = photo
        self.label_img_resize.grid(column=5, row=4)

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.label = Label(self.labelFrame, text="")
        self.label.grid(column=1, row=0)
        self.label.configure(text=self.filename)

        self.type_img = Label(self, text="Original Image")
        self.type_img.grid(column=0, row=3)

        img = Image.open(self.filename)
        photo = ImageTk.PhotoImage(img)

        self.label_img = Label(self, image=photo)
        self.label_img.image = photo
        self.label_img.grid(column=0, row=4)


root = Root()
root.mainloop()
