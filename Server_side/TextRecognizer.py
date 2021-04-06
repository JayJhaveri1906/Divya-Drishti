import pytesseract  # 5.4.0
import cv2  # 4.1.0


class TextRecognizer():

    def __init__(self):
        self.text = None
        self.size = 500

    def ocr2(self, img):
        im = img
        # im = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # Uncomment the line below to provide path to tesseract manually
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

        # Define config parameters.
        # '-l eng'  for using the English language
        # '--oem 1' for using LSTM OCR Engine
        # config = ('-l eng --oem 1 --psm 3')
		#
        # # Read image from disk
        # # im = cv2.imread(imPath, cv2.IMREAD_COLOR)
        # # im = cv2.imread(imPath, 0)
        # # Run tesseract OCR on image
        # pytesseract.pytesseract.tesseract_cmd = 'D:\\Softwares\\Tesseract-ocr\\tesseract.exe'
        # text = pytesseract.image_to_string(im)
        # text = pytesseract.image_to_string(im, config=config)
        # # Print recognized text
        # print(text)

        config = r"--oem 3 --psm 6"

        # Read image from disk
        # im = cv2.imread(imPath, cv2.IMREAD_COLOR)
        # im = cv2.imread(imPath, 0)
        # Run tesseract OCR on image
        # pytesseract.pytesseract.tesseract_cmd = 'D:\\Softwares\\Tesseract-ocr\\tesseract.exe'
        # text = pytesseract.image_to_string(im)
        self.text = pytesseract.image_to_string(im, config=config)
        # Print recognized text
        print("new\n", self.text)

        cv2.imshow("nub", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    """ Tesseract OCR works great on lower sized images. Hence resizing is an important preprocessing step. """

    def ocr(self, img):
        self.ocr2(img)
        # self.im = img
        # self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        # self.im = cv2.resize(self.im, (self.size, self.size))
        # config = ('-l eng --oem 1 --psm 3')
        # self.text = pytesseract.image_to_string(self.im, config=config)
        # print("SELFFFFFFFF TEXTTT",self.text)
        return self.text


""" im = cv2.imread("/Users/dhavalbagal/Desktop/BE-PROJECT/Sahara/TestImages/20200128_223117.jpg",0)
a= TextRecognizer()
text = a.ocr(im)

print("\n\n",text) """