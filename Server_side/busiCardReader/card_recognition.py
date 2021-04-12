import cv2
import jsonpickle
import pytesseract

# import card_region_detector as region_detector
from .pattern_recognition import common_name_recognition as name_recog
from .pattern_recognition.address_name_recognition import *
from .pattern_recognition.email_recognition import is_email
from .pattern_recognition.job_title_recognition import is_job_title
from .pattern_recognition.phone_recognition import is_phone
from .pattern_recognition.website_recognition import is_website
from .pattern_recognition.company_name_recognition import is_company_name

try:
    import Image
except ImportError:
    from PIL import Image

from .contact import Contact

DEBUG = False


def recognize_contact(img_path):
    # txt = extract_2(img_path)
    txt = """KAVIN KUMAR J
4 Home Loan Sales Manager
HOME +91 9080663743

LOAN U +91 9698641603
% kavin.sbihomeloan@gmail.com
State Bank of India
CP Ramaswamy lyer Road,
Sriram Colony, Abiramapuram,
Chennai - 600018, Tamil Nadu."""
    print("abhay",txt)
    tokens = tokenizer(txt)
    contact = Contact()

    contact.name = name_recog.find_best_guessed_name(tokens)[2]

    for token in tokens:
        if is_address(token):
            contact.addr.append(token)
        if is_email(token):
            contact.emails.append(token)
        if is_phone(token):
            contact.phones.append(token)
        if is_job_title(token):
            contact.job_title = token
        if is_website(token):
            contact.website = token
        if is_company_name(token):
            contact.company = token
    print(tokens)
    return contact


# def extract(img_path):
#     txt = pytesseract.image_to_string(Image.open(img_path))
#     return txt


# # Extract business card border, then recognize text
# def extract_2(img_path):
#     image_size = 500
#
#     # Read
#     img = cv2.imread(img_path)
#     orig_width, orig_height, _ = img.shape
#
#     # Make image smaller for faster processing
#     scale = orig_width / image_size
#     resized_img = cv2.resize(img, (image_size, int(orig_height / scale + 1)), None)
#
#     # Crop text region
#     cropped = region_detector.crop_text_region(resized_img)
#
#     # Restore Original region
#     orig_crop = [int(round(x * scale)) for x in cropped]
#     text_region = img[orig_crop[1]: orig_crop[3], orig_crop[0]: orig_crop[2]]
#     pytesseract.pytesseract.tesseract_cmd = 'D:\\Softwares\\Tesseract-ocr\\tesseract.exe'
#
#     # Convert to Image object to make tesseract happy
#     pil_img = Image.fromarray(text_region)
#     txt = pytesseract.image_to_string(pil_img, lang='eng')
#
#     global DEBUG
#     if DEBUG:
#         pil_img.show()
#         print('txt', txt)
#         cv2.rectangle(resized_img, (cropped[0], cropped[1]), (cropped[2], cropped[3]), (0, 255, 0), 1)
#         cv2.imshow('resized', resized_img)
#
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#     return txt


def tokenizer(txt):
    lines = txt.split("\n")
    tokens = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            tokens.append(line)

    return tokens

class CardRecog:

    def __init__(self):
        self.acceptedVars = ["addr","emails", "name", "company", "job_title", "phones", "website"]
        self.tmpDic = {"addr": "Address", "emails": "Email", "name": "Name", "company": "Company's Name",
                  "job_title": "Job title", "phones": "Phone Number", "website":"Website"}

    def cardRecog(self,txt):
        # txt = """KAVIN KUMAR J
        #         4 Home Loan Sales Manager
        #         HOME +91 9080663743
        #
        #         LOAN U +91 9698641603
        #         % kavin.sbihomeloan@gmail.com
        #         State Bank of India
        #         CP Ramaswamy lyer Road,
        #         Sriram Colony, Abiramapuram,
        #         Chennai - 600018, Tamil Nadu."""
        # print("NEWWW TXT")
        tokens = tokenizer(txt)
        contact = Contact()

        contact.name = name_recog.find_best_guessed_name(tokens)[2]

        for token in tokens:
            if is_address(token):
                contact.addr.append(token)
            if is_email(token):
                contact.emails.append(token)
            if is_phone(token):
                contact.phones.append(token)
            if is_job_title(token):
                contact.job_title = token
            if is_website(token):
                contact.website = token
            if is_company_name(token):
                contact.company = token
        print("In cardReader")
        fullDic = eval(jsonpickle.encode(contact))
        print(fullDic)

        if fullDic:
            return fullDic
        else:
            fullDic = {}
            return fullDic

    def fullCardRecog(self,fullDic):
        print("In Full cardReader")
        print(fullDic)
        strg = ""
        for i in fullDic:
            if i in self.acceptedVars:
                tmpAns = fullDic[i]
                if tmpAns=="N/A" or tmpAns==[]:
                    pass
                else:
                    strg += self.tmpDic[i] +" is "+str(tmpAns)+"\n"
        if strg:
            return strg
        else:
            return "No card found"

        # print(tokens)
        # return contact


if __name__ == '__main__':
    sample_path = '../samples/bc_ref/1.png'
    contact = recognize_contact(sample_path)
    print((' ' * 30))
    print((' * ' * 30))
    # print(type(contact),contact)
    # print((jsonpickle.encode(contact)))
    # print("in Dic")
    # print(type((eval(jsonpickle.encode(contact)))))
    print((eval(jsonpickle.encode(contact))))

