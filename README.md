Image Editor

A command-line image editor in Python that implements core image-processing operations directly on pixel lists.

What It Does
- Converts RGB images to grayscale using weighted color channels.
- Blurs images using an odd-sized box kernel.
- Resizes images (minimum 2x2) with bilinear interpolation.
- Rotates images 90 degrees left or right.
- Detects edges using blurring and local block thresholding.
- Quantizes color shades to N levels (N >= 2).
- Previews the image and saves the result on exit.

Tools & Languages
- Python
- Pillow (PIL) via ex6_helper
- Standard library modules (sys, copy, typing)

How to Run
1. Make sure pillow is installed
2. Run with an image path:
   python image_editor.py path/to/image.png
3. Use the menu (1-8) to edit, preview, and save on exit (option 8).
Example:
>>> python image_editor.py girl_cartoon.png
>>> 5
>>> 1,5,5
>>> 7
>>> 8
>>> girl_edges.png
