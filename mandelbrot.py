# Austin Cubbage
# 3/11/15
# The Mandelbrot fractal program. Render your favorite spots!

import helper
import complex
import tkinter as tk
import os
from PIL import Image, ImageDraw

# The first number in the tuple is the R/G/B of the background/outside, the
# second number is the R/G/B of the mandelbrot spirals.
MAX = 255
RED_VALUES = 102, 255, 0
GREEN_VALUES = 255, 51, 0
BLUE_VALUES = 102, 102, 0

UPPER_HEX_RANGE = 16
PIXEL_WIDTH = 1
ZOOM_SHIFT = 4
pixel_r = PIXEL_WIDTH // 2

class Mandelbrot:

    # Pre: Takes the width and height of the canvas.
    def __init__(self, w_width, w_height):
        self.w_width = w_width
        self.w_height = w_height
        self.my_helper = None

        self.root_window = tk.Tk()
        self.canvas = tk.Canvas(self.root_window, width = self.w_height,
                                height = self.w_height)

        self.new_image = Image.new("RGB", (self.w_width, self.w_height),
                           (MAX, MAX, MAX))
        self.draw = ImageDraw.Draw(self.new_image, "RGB")
        self.center_x, self.center_y = 0, 0
        self.mb_width = 4

    # Pre:  Takes the escape value of a pixel, the iterations it ran in the
    #       recursive function
    # Post: Returns a string that represents that pixels color, as well as the rgb value.
    def generate_color(self, escape_value):
        i = escape_value / MAX
        SEPERATOR = 0.5
        r, g, b = MAX, MAX, MAX
        ADD_ZERO_RANGE = list(range(0, UPPER_HEX_RANGE))
        if i < SEPERATOR:
            r = int((RED_VALUES[0] * (1 - i) + (RED_VALUES[1] * i)))
            g = int((GREEN_VALUES[0] * (1 - i) + (GREEN_VALUES[1] * i)))
            b = int((BLUE_VALUES[0] * (1 - i) + (BLUE_VALUES[1] * i)))


        if i > SEPERATOR:
            r = int((RED_VALUES[1] * (1 - i) + (RED_VALUES[2] * i)))
            g = int((GREEN_VALUES[1] * (1 - i) + (GREEN_VALUES[2] * i)))
            b = int((BLUE_VALUES[1] * (1 - i) + (BLUE_VALUES[2] * i)))

        r_hex = hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]

        if r in ADD_ZERO_RANGE or len(r_hex) == 1:
            r_hex = "0" + r_hex
        if g in ADD_ZERO_RANGE or len(g_hex) == 1:
            g_hex = "0" + g_hex
        if b in ADD_ZERO_RANGE or len(b_hex) == 1:
            b_hex = "0" + b_hex
        return "#" + r_hex + g_hex + b_hex, (r, g, b)

    # Pre:  Takes the left mouse click event
    # Post: Will zoom in on the location that the user clicked on.
    def handle_zoom_in(self, event):
        self.center_x, self.center_y = self.my_helper.convert_coords(event.x,
                                                                     event.y)
        self.mb_width /= ZOOM_SHIFT
        print(self.center_x, self.center_y, self.mb_width)
        self.generate_mandelbrot(self.center_x, self.center_y, self.mb_width)

    # Pre:  Takes the right mouse click event
    # Post: Will zoom out from the location that the user clicked on.
    def handle_zoom_out(self, event):
        self.center_x, self.center_y = self.my_helper.convert_coords(event.x,
                                                                     event.y)
        self.mb_width *= ZOOM_SHIFT
        print(self.center_x, self.center_y, self.mb_width)
        self.generate_mandelbrot(self.center_x, self.center_y, self.mb_width)

    # Pre:  None
    # Post: Saves the coordinates that you are at in a text file
    def save_coordinates(self):
        coord_string = ("Center x: " + str(self.center_x) + "\n" +
                        "Center y: " + str(self.center_y) + "\n" +
                        "Width   : " + str(self.mb_width) + "\n")
        file_name = "coords.txt"
        my_file = open(file_name, "a")
        my_file.write(coord_string)

    # Pre:  None
    # Post: Creates an image in the directory of the current canvas.
    def save_image(self):
        my_file = "render.jpg"
        self.new_image.save(my_file)

    # Pre:  Takes the center x and the
    #       center y of the square being generated, and the width of the
    #       mandelbrot generation.
    # Post: Will render the mandelbrot generation in the canvas. Also
    #       will create a new window if this generation is a zoom.
    def generate_mandelbrot(self, center_x, center_y, mb_width):
        self.canvas.delete(tk.ALL)        
        self.canvas.pack()

        self.center_x, self.center_y = center_x, center_y
        self.mb_width = mb_width

        x_list = list(range(0, self.w_width + 1))
        y_list = list(range(0, self.w_height + 1))

        lower_a = self.center_x - self.mb_width / 2
        upper_a = self.center_x + self.mb_width / 2
        lower_b = self.center_y - self.mb_width / 2
        upper_b = self.center_y + self.mb_width / 2

        self.my_helper = helper.Helper(self.w_width, self.w_height,
                                       (lower_a, upper_a),
                                       (lower_b, upper_b))

        main_menu = tk.Menu(self.root_window)
        menu = tk.Menu(main_menu,fg = "green",
                       bg = "black", relief = "raised")
        menu.add_command(label = "Save Coordinates",
                         command = self.save_coordinates)
        menu.add_separator()
        menu.add_command(label = "Save bImage", command = self.save_image)
        main_menu.add_cascade(label = "File", menu = menu)
        self.root_window.config(menu = main_menu)

        for x in x_list:
            #print("\r" + str(x))
            for y in y_list:
                a, b = self.my_helper.convert_coords(x, y)

                new_complex = complex.Complex(a, b)
                escape_value = self.my_helper.compute_num_iterations(new_complex, new_complex, 0)

                color_string, rgb = self.generate_color(escape_value)
                x1, y1 = x - pixel_r, y - pixel_r
                x2, y2 = x + pixel_r, y + pixel_r
                self.canvas.create_rectangle(x1, y1, x2, y2, fill = color_string, outline = color_string)
                self.draw.rectangle((x1, y1, x2, y2), fill = rgb, outline = rgb)
        self.canvas.update()
        self.canvas.bind("<ButtonRelease-1>", self.handle_zoom_in)
        self.canvas.bind("<ButtonRelease-3>", self.handle_zoom_out)
        self.root_window.mainloop()

WIDTH, HEIGHT = 800, 800
my_mb = Mandelbrot(WIDTH, HEIGHT)


print("PLEASE ENTER THE CENTER X AND Y, AND THE MANDELBROT WIDTH:")
center_x = float(input("Center x: "))
center_y = float(input("Center y: "))
mb_width = float(input("Fractal Width: "))
my_mb.generate_mandelbrot(center_x, center_y, mb_width)



