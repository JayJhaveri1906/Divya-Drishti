import cv2  # 4.1.0
import numpy as np
import webcolors
from dominant_color_detection import detect_colors
from PIL import Image

class ColorRecognizer:

    def __init__(self):
        self.simpleColor_dic = {"aliceblue": "light blue", "antiquewhite": "skin", "cyan": "light blue",
                           "aquamarine": "light green", "azure": "dark blue", "beige": "skin", "bisque": "skin",
                           "black": "black", "blanchedalmond": "skin", "blue": "blue", "blueviolet": "purple",
                           "brown": "brown", "burlywood": "skin", "cadetblue": "blue", "chartreuse": "light green",
                           "chocolate": "brown", "coral": "orange", "cornflowerblue": "light blue",
                           "cornsilk": "yellow", "crimson": "dark", "darkblue": "dark blue", "darkcyan": "dark green",
                           "darkgoldenrod": "yellow", "darkgrey": "black", "darkgreen": "dark green",
                           "darkkhaki": "yellow", "darkmagenta": "purple", "darkolivegreen": "dark green",
                           "darkorange": "orange",
                           "darkorchid": "purple", "darkred": "dark red", "darksalmon": "pink",
                           "darkseagreen": "dark green", "darkslateblue": "dark blue", "darkslategrey": "dark blue",
                           "darkturquoise": "light blue",
                           "darkviolet": "purple", "deeppink": "pink", "deepskyblue": "light blue", "dimgrey": "gray",
                           "dodgerblue": "dark blue", "firebrick": "dark red",
                           "floralwhite": "skin", "forestgreen": "green", "magenta": "pink", "gainsboro": "gray",
                           "ghostwhite": "white", "gold": "yellow", "goldenrod": "yellow",
                           "grey": "gray", "green": "green", "greenyellow": "light green", "honeydew": "light green",
                           "hotpink": "pink", "indianred": "red", "indigo": "dark blue",
                           "ivory": "skin", "khaki": "yellow", "lavender": "purple", "lavenderblush": "purple",
                           "lawngreen": "light green", "lemonchiffon": "yellow", "lightblue": "lightblue",
                           "lightcoral": "skin", "lightcyan": "light blue", "lightgoldenrodyellow": "skin",
                           "lightgrey": "gray", "lightgreen": "light green",
                           "lightpink": "pink", "lightsalmon": "skin", "lightseagreen": "light blue",
                           "lightskyblue": "light blue", "lightslategrey": "gray", "lightsteelblue": "light blue",
                           "lightyellow": "yellow", "lime": "light green", "limegreen": "light green", "linen": "skin",
                           "maroon": "dark red", "mediumaquamarine": "light blue", "mediumblue": "blue",
                           "mediumorchid": "purple", "mediumpurple": "dark blue", "mediumseagreen": "green",
                           "mediumslateblue": "blue", "mediumspringgreen": "light green",
                           "mediumturquoise": "light blue",
                           "mediumvioletred": "pink", "midnightblue": "dark blue", "mintcream": "white",
                           "mistyrose": "pink", "moccasin": "skin", "navajowhite": "skin", "navy": "blue",
                           "oldlace": "white",
                           "olive": "green", "olivedrab": "green", "orange": "orange", "orangered": "orange",
                           "orchid": "pink", "palegoldenrod": "skin", "palegreen": "green",
                           "paleturquoise": " light blue", "palevioletred": "pink",
                           "papayawhip": "skin", "peachpuff": "pink", "peru": "brown", "pink": "pink", "plum": "purple",
                           "powderblue": "light blue", "purple": "purple", "red": "red", "rosybrown": "pink",
                           "royalblue": "dark blue",
                           "saddlebrown": "brown", "salmon": "pink", "sandybrown": "yellow", "seagreen": "dark green",
                           "seashell": "skin", "sienna": "brown", "silver": "grey", "skyblue": "light blue",
                           "slateblue": "dark blue", "slategrey": "dark blue", "snow": "white", "springgreen": "light green",
                           "steelblue": "dark blue", "tan": "brown", "teal": "dark blue",
                           "thistle": "purple", "tomato": "orange", "turquoise": "light blue", "violet": "purple",
                           "wheat": "yellow", "white": "white",
                           "whitesmoke": "white", "yellow": "yellow", "yellowgreen": "green"}


    def closest_colour(self, requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(self, requested_colour):
        try:
            print(type(webcolors.rgb_to_name))
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = self.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    def recColor(self, img):
        k = 3
        img_path = Image.fromarray(img)
        img_path.show()
        colors, ratios = detect_colors(img_path, k)
        print("COLORRRR",colors)
        print(colors, "\n", ratios)

        tmp = webcolors.hex_to_rgb(colors[0])

        # tmp = hex_to_rgb("#feb504")
        print(tmp)
        requested_colour = tmp
        actual_name, closest_name = self.get_colour_name(requested_colour)

        print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

        try:
            closest_name = self.simpleColor_dic[closest_name]
            print("Color is "+str(closest_name))

        except:
            print("complex name is "+ str(closest_name))

        if closest_name == "white" and len(colors) > 1: # for cases of white background
            tmp = webcolors.hex_to_rgb(colors[1])

            # tmp = hex_to_rgb("#feb504")
            print(tmp)
            requested_colour = tmp
            actual_name, closest_name = get_colour_name(requested_colour)

            print("Actual colour name:", actual_name, ", closest colour name:", closest_name)
            try:
                closest_name = self.simpleColor_dic[closest_name]
                return("Color is "+str(closest_name))

            except:
                return("complex name is "+ str(closest_name))
        return("Color is "+str(closest_name))


if __name__ == "__main__":
    simpleColor_dic = {"aliceblue": "light blue", "antiquewhite": "skin", "cyan": "light blue",
                            "aquamarine": "light green", "azure": "dark blue", "beige": "skin", "bisque": "skin",
                            "black": "black", "blanchedalmond": "skin", "blue": "blue", "blueviolet": "purple",
                            "brown": "brown", "burlywood": "skin", "cadetblue": "blue", "chartreuse": "light green",
                            "chocolate": "brown", "coral": "orange", "cornflowerblue": "light blue",
                            "cornsilk": "yellow", "crimson": "dark", "darkblue": "dark blue", "darkcyan": "dark green",
                            "darkgoldenrod": "yellow", "darkgrey": "black", "darkgreen": "dark green",
                            "darkkhaki": "dark green", "darkmagenta": "purple", "darkolivegreen": "dark green",
                            "darkorange": "orange",
                            "darkorchid": "purple", "darkred": "dark red", "darksalmon": "pink",
                            "darkseagreen": "dark green", "darkslateblue": "dark blue", "darkslategrey": "gray",
                            "darkturquoise": "light blue",
                            "darkviolet": "purple", "deeppink": "pink", "deepskyblue": "light blue", "dimgrey": "gray",
                            "dodgerblue": "dark blue", "firebrick": "dark red",
                            "floralwhite": "skin", "forestgreen": "green", "magenta": "pink", "gainsboro": "gray",
                            "ghostwhite": "white", "gold": "yellow", "goldenrod": "yellow",
                            "grey": "gray", "green": "green", "greenyellow": "light green", "honeydew": "light green",
                            "hotpink": "pink", "indianred": "red", "indigo": "dark blue",
                            "ivory": "skin", "khaki": "yellow", "lavender": "purple", "lavenderblush": "purple",
                            "lawngreen": "light green", "lemonchiffon": "yellow", "lightblue": "lightblue",
                            "lightcoral": "skin", "lightcyan": "light blue", "lightgoldenrodyellow": "skin",
                            "lightgrey": "gray", "lightgreen": "light green",
                            "lightpink": "pink", "lightsalmon": "skin", "lightseagreen": "light blue",
                            "lightskyblue": "light blue", "lightslategrey": "gray", "lightsteelblue": "light blue",
                            "lightyellow": "yellow", "lime": "light green", "limegreen": "light green", "linen": "skin",
                            "maroon": "dark red", "mediumaquamarine": "light blue", "mediumblue": "blue",
                            "mediumorchid": "purple", "mediumpurple": "dark blue", "mediumseagreen": "green",
                            "mediumslateblue": "blue", "mediumspringgreen": "light green",
                            "mediumturquoise": "light blue",
                            "mediumvioletred": "pink", "midnightblue": "dark blue", "mintcream": "white",
                            "mistyrose": "pink", "moccasin": "skin", "navajowhite": "skin", "navy": "blue",
                            "oldlace": "white",
                            "olive": "green", "olivedrab": "green", "orange": "orange", "orangered": "orange",
                            "orchid": "pink", "palegoldenrod": "skin", "palegreen": "green",
                            "paleturquoise": " light blue", "palevioletred": "pink",
                            "papayawhip": "skin", "peachpuff": "pink", "peru": "light brown", "pink": "pink",
                            "plum": "purple",
                            "powderblue": "light blue", "purple": "purple", "red": "red", "rosybrown": "pink",
                            "royalblue": "dark blue",
                            "saddlebrown": "brown", "salmon": "pink", "sandybrown": "yellow", "seagreen": "dark green",
                            "seashell": "skin", "sienna": "brown", "silver": "grey", "skyblue": "light blue",
                            "slateblue": "dark blue", "slategrey": "gray", "snow": "white",
                            "springgreen": "light green",
                            "steelblue": "dark blue", "tan": "brown", "teal": "dark blue",
                            "thistle": "purple", "tomato": "orange", "turquoise": "light blue", "violet": "purple",
                            "wheat": "yellow", "white": "white",
                            "whitesmoke": "white", "yellow": "yellow", "yellowgreen": "green"}

    # print(len(simpleColor_dic))
    ### VERIFICATION
    # lis = ['aliceblue', 'antiquewhite', 'cyan', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'magenta', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    # for i in lis:
    #   closest_name = i
    #   print("initial",closest_name)
    #   try:
    #     closest_name = simpleColor_dic[closest_name]
    #     print("final",closest_name)

    #   except:
    #     print("no key found", closest_name)



    k = 3
    img_path = 'unknown.png'

    colors, ratios = detect_colors(img_path, k)
    print(colors, "\n", ratios)

    tmp = webcolors.hex_to_rgb(colors[0])

    # tmp = hex_to_rgb("#feb504")
    print(tmp)
    requested_colour = tmp
    actual_name, closest_name = get_colour_name(requested_colour)

    print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

    try:
        closest_name = simpleColor_dic[closest_name]
        print("final", closest_name)

    except:
        print("no key found", closest_name)

    if closest_name == "white" and len(colors) > 1:
        tmp = webcolors.hex_to_rgb(colors[1])

        # tmp = hex_to_rgb("#feb504")
        print(tmp)
        requested_colour = tmp
        actual_name, closest_name = get_colour_name(requested_colour)

        print("Actual colour name:", actual_name, ", closest colour name:", closest_name)
        try:
            closest_name = simpleColor_dic[closest_name]
            print("final", closest_name)

        except:
            print("no key found", closest_name)
    print("Simple Color Name:", closest_name)


