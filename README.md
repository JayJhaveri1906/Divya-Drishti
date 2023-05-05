# Divya-Drishti: An Independent Aid for the Visually Impaired
[![IMAGE ALT TEXT HERE](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=lRjCKhczHtY)


- The Objective of this system is to help/guide the **visually challenged people** with the help of a smart device using an Android Phone. 

- This device will help the visually challenged person to get greater sense of awareness of surroundings around him/her and will also help him/her by protecting them against frauds.

- What makes this device innovative is that the device is **completely Internet Free** and also helps in effective communication with the help of Voice Commands as this is the
only medium through which a visually challenged person can effectively communicate with an **external device**.

This device has successfully managed to implement multiple daily usage features like

1. Currency Detection
2. Bill Reading 
3. Text Summarization
4. Mask Detection
5. Color Detection 
6. Buisness Card Reader 

In a single standalone portable system.

---
We go in detail about out methodology in our [research paper](https://dx.doi.org/10.2139/ssrn.3867707)


For a very detailed documentation of the project, please refer to this [word document](https://docs.google.com/document/d/1fwOqflFFXYsEYjk2FMS-T_B69LDfOEEvVPOvCZo3veM/edit?usp=sharing)


Summarized video:\
<a href="https://www.youtube.com/watch?v=lRjCKhczHtY
" target="_blank"><img src="https://i.ytimg.com/vi/lRjCKhczHtY/maxresdefault.jpg" 
alt="Aatmanirbhar Samakraman: Auto File Sync App" width="426" height="240" border="10" /></a>


---
A brief overview:

The one project that is very close to my heart is Divya Drishti. 

The motivation for it actually goes all the way back to high school, where a guy around the age of my grandpa startled me in the middle of the road and asked for my help to cross the road. This, combined with my fascination with what google photos are able to achieve, gave birth to the idea of DD. 

To summarize, Divya Drishti is an off-the-grid, Voice-activated standalone AIOT application/device hosted on a Raspberry Pi4 connected to any Android phone to help Visually Impaired People accurately detect Currency notes, colors, and everyday objects. 

The main aim was to achieve a complete End to End Edge processing device that is not dependent on the cloud and can be used in places with low or no connectivity!

I was fortunate enough to find team members who were as excited as me about my vision, and we secured the funding under the Mumbai University Minor Research Grant Program.

To summarize the product from a technical perspective: 
The product consists of two parts:
1. Python-based server architecture hosted on a pocket-friendly Raspberry Pi4.
2. Android-Java-based simple Android application for the end user to use. Our intended end users consisted of anyone with visual impairments needing a device to help with their daily mundane tasks. We called them VIPs (Visually Impaired People).

To give a brief overview, a VIP, after opening the Android application, could simply tap anywhere on the screen to capture an image using the Android phone's camera and give audio commands. The Android application would automatically and quickly convert the speech commands to raw text and send the captured image and the raw text to the Raspberry Pi for processing.

The audio commands supported were:
1. Detect currency/ Total Currency in hand: My team managed to train an Indian currency detection model which is able to accurately classify each denomination note in the given image with 95+% accuracy. We trained it using Google's Vision API on the GCP console.
2. Read Text: We used Tesseract OCR to read text from the image
3. Summarize Text: This calls option 2, then we implemented a text summarizer using NLTK
4. Read a business card: To build this, I used my previous experience from a data extraction project I used to build my hackathon-winning OCR app for Global Parli NGO to convert Devanagari scripted documents into an editable Excel format. Here, after reading the business card, it would match the detected text with the most common formats of business cards and then read in a structured format with labels: "Name: Jay Jhaveri, Address: XYZ, Company: ABC."
5. Bill Reading: To take it up a notch, to detect if the VIP is being scammed by giving a fake bill with the total amount printed wrong. Upon receiving the text, python's regex (Regular Expressions) library converts the plain text into records split by a new line. If the number of records with FOUR floating point numbers (Qty, MRP, Rate, Amount) exceeds the system-defined threshold, then the image can be considered to be a supermarket bill and can be processed further. Once the system determines that the image is of a supermarket bill, it applies various permutations (4P2) and checks if the multiplication of two floating point numbers matches one of the four floating point numbers. Based on this, the module finds the mapping of the four floating point numbers to Qty, MRP, Rate, and Amount. The remaining text, apart from these 4 numbers, is considered to be the product name. 
6. Mask detection: Because DD was developed in the midst of the Covid 19 pandemic, It detected if the person standing in the frame is wearing a mask or not. The model was trained very similarly to how the currency model was trained.
7. Color detection: self-explanatory, used OpenCV pixel color detection to get the RGB, then bucketed these RGB values in 16 primary colors.
8. Object detection: We used YoloV5 to cover a variety of everyday objects such as pens, books, etc. Thinking that if a VIP dropped a common object and isn't able to find it, he would be able to use the app to at least detect in which general area the object dropped!


We presented our application in front of 10 members of the members of National Association for the Blind (NAB), India, and received valuable feedback, including a request to support the detection of coins and to also speak out about the general direction the detected object is in the frame. 

We ended up publishing our work in the SSRN journal as part of the 4th International Conference on Advances in Science & Technology (ICAST2021), highlighting how we managed to incorporate all of this in only a sub 8000 Rupees product and achieve well above 400% in a net cost reduction compared to products made by OrCam and other competitors. 

You may read more in detail at: https://dx.doi.org/10.2139/ssrn.3867707
Black book: https://docs.google.com/document/d/1fwOqflFFXYsEYjk2FMS-T_B69LDfOEEvVPOvCZo3veM/edit?usp=sharing
