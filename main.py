from asyncio.windows_events import NULL
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from preprocess import *
from hog import *
import csv
from recognition import Recognition


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Handwriting recognition")
        self.minsize(800, 500)

        self.labelFrame = LabelFrame(text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.labelImage = LabelFrame()
        self.labelImage.grid(column=0, row=2)

        self.entryLetter = Entry(self.labelFrame, font=('Arial', 20), show="", width=10)
        self.entryLetter.grid(column=1, row=8)

        self.addSample = Button(self.labelFrame, text="Add sample", command=self.extractFeatures)
        self.addSample.grid(column=2, row=8, padx=5, pady=20)

        self.openFileBtn()
        self.rgbToBinBtn()
        # self.thinImgBtn()
        self.cropImgBtn()
        self.resizeImgBtn()
        self.recognitionBtn()
        self.exitBtn()

    def openFileBtn(self):
        self.btn_open_file = Button(
            self.labelFrame, text="Browse A File", command=self.fileDialog, width=20, height=2)
        self.btn_open_file.grid(column=1, row=1)

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir="C:/Users/Admin/Downloads/dpt/data", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.labelFrame.configure(text=self.filename)

        self.type_img = Label(self.labelImage, text="Original Image")
        self.type_img.grid(column=0, row=1)

        img = Image.open(self.filename)
        photo = ImageTk.PhotoImage(img)

        self.label_img = Label(self.labelImage, image=photo)
        self.label_img.image = photo
        self.label_img.grid(column=0, row=2)
        self.label_img_bin.configure(image='')
        self.label_img_crop.configure(image='')
        self.label_img_resize.configure(image='')
        self.label_result.configure(text='')
        # self.label_img_bin.configure(image='')

    def exitBtn(self):
        self.btn_exit = Button(
            self.labelFrame, text="Exit", command=exit, width=20, height=2)
        self.btn_exit.grid(column=7, row=1)

    def rgbToBinBtn(self):
        # convert rgb img to binary img
        self.btn_process = Button(
            self.labelFrame, text="Convert to Binary", command=self.binaryImg, width=20, height=2)
        self.btn_process.grid(column=2, row=1)

    def binaryImg(self):
        pre_process_img = PreProcess(self.filename)
        pre_process_img.binaryImage()

        self.type_img = Label(self.labelImage, text="Binary Image")
        self.type_img.grid(column=1, row=1)

        img = Image.open('binary.png')
        photo = ImageTk.PhotoImage(img)

        self.label_img_bin = Label(self.labelImage, image=photo)
        self.label_img_bin.image = photo
        self.label_img_bin.grid(column=1, row=2)

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
            self.labelFrame, text="Crop Image", command=self.croppingImg, width=20, height=2)
        self.btn_crop.grid(column=4, row=1)

    def croppingImg(self):
        pre_process_img = PreProcess('binary.png')
        pre_process_img.cropImg()
        self.type_img = Label(self.labelImage, text="Cropping Image")
        self.type_img.grid(column=2, row=1, padx=40)

        crop_image = Image.open('crop_img.png')
        photo = ImageTk.PhotoImage(crop_image)
        self.label_img_crop = Label(self.labelImage, padx=40)
        self.label_img_crop.configure(image=photo)
        self.label_img_crop.image = photo
        self.label_img_crop.grid(column=2, row=2)

    def resizeImgBtn(self):
        self.btn_crop = Button(
            self.labelFrame, text="Resize Image", command=self.resizingImg, width=20, height=2)
        self.btn_crop.grid(column=5, row=1)

    def resizingImg(self):
        pre_process_img = PreProcess('binary.png')
        pre_process_img.resizeImg()
        self.type_img = Label(self.labelImage, text="Resize", padx=40)
        self.type_img.grid(column=3, row=1)

        resize_img = Image.open('resize_img.png')
        photo = ImageTk.PhotoImage(resize_img)
        self.label_img_resize = Label(self.labelImage, image=photo, padx=40)
        self.label_img_resize.image = photo
        self.label_img_resize.grid(column=3, row=2)

    def recognitionBtn(self):
        self.btn_result = Button(
            self.labelFrame, text="Recognition", command=self.recognition, width=20, height=2)
        self.btn_result.grid(column=6, row=1)

    def recognition(self):
        recog = Recognition()
        result = recog.recognition()

        # print(result[0][1])
        self.label_result = Label(
            self, text="Result: " + result[0][1], font=('Arial', 20))
        self.label_result.grid(column=0, row=6)

    def extractFeatures(self):
        hog_img = Hog()
        letter = self.entryLetter.get()
        data = hog_img.extractFeature('resize_img.png')

        with open('data.csv', 'a+', newline='') as datacsv:
            writer = csv.writer(datacsv, dialect='excel')
            output_row = [letter]
            output_row.extend(data)
            writer.writerow(output_row)

root = Root()
root.mainloop()
