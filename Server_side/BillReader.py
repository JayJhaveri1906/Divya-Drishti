import cv2 #4.1.0
import re   #2.2.1
# from TextRecognizer import TextRecognizer
import pytesseract  # 5.4.0

class BillReader:

    def __init__(self):
        self.text = ""
        # self.size = 500
        # self.textRecognizer = TextRecognizer()
        # self.products = dict()


    """ Note: A product name in a bill is always followed by a floating number indicating either the tax or the amount.\
        Hence fetching all the characters before the first floating number will give the product name."""
    # def extractProductNames(self):
    #     productNameRegex = '^(.*?)[0-9]+[.][0-9]+'
    #     productPrice = '[0-9]+[.][0-9]+'
    #
    #     """ Every record contains productName followed by the tax amount, quantity, price etc."""
    #     print("text: ", self.text)
    #     records = self.text.splitlines()
    #
    #     for record in records:
    #         try:
    #             """ When capturing a group in a regular expression, you need to put parentheses around the group that you aim to capture. \
    #                 Also, you need to pass the index of the group you want to capture to the group() method. """
    #             productName = re.search(productNameRegex, record).group(1)
    #             print(productName)
    #             """ Assumption: Last floating number in a record is the price of the product. """
    #             self.products[productName] = re.findall(productPrice, record)[-1]
    #         except:
    #             """ Ignore if no product is found in a record """
    #             pass
    #
    #
    # def readBill(self, img):
    #     print("in read bill")
    #     self.im = img
    #     self.text = self.textRecognizer.ocr(self.im)
    #     self.extractProductNames()
    #     if len(self.products)!=0:
    #         reply = ""
    #         for name, price in self.products.items():
    #             reply+= name+" costs INR "+str(price)+". "
    #     else:
    #         reply = "I am not able to read the bill. Please try again."
    #     return reply


    # JHOL METHOD, only zoom on bottom right of bill
    def readBill(self, img):
        config = r"--oem 3 --psm 6 digits"

        # Read image from disk
        # im = cv2.imread(imPath, cv2.IMREAD_COLOR)
        # im = cv2.imread(imPath, 0)
        # Run tesseract OCR on image
        # pytesseract.pytesseract.tesseract_cmd = 'D:\\Softwares\\Tesseract-ocr\\tesseract.exe'
        # text = pytesseract.image_to_string(im)
        self.text = pytesseract.image_to_string(img, config=config)
        # Print recognized text
        print("new\n", self.text)
        lst = self.text.split()
        print(lst)
        amt = 0
        for i in lst:
            try:
               if float(i)>amt:
                   amt = float(i)
            except:
                print("failed number",i)
                pass
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return "Total amount is "+str(amt)

""" im = cv2.imread("/Users/dhavalbagal/Desktop/BE-PROJECT/temp4.jpg",0)
a= BillReader()
p = a.readBill(im) 
print(p) """
