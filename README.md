# glitcher
Manipulates images to give them a pseudo-glitch effect. In a really unnecessary, dumb way.

In actuality, it's just changing individual pixels' values a certain number of times. It selects each value randomly, then replaces them with a random, different value (hopefully!). Like pixels remain alike through all permutations. This effect is probably more noticeable in images with higher resolutions.

Ensure that you have Pillow installed! If you can `import PIL` without getting an error, you're good. If you do get an error, use `pip install Pillow`. You'll also need `pyvips`.

Get started by accessing the script's location in your terminal, then enter a command with the following arguments:

```
glitcher.py image_location output_filename -o output_destination -m mutations -r replacements_per_pass -f frames -k
```

- `image_location` is a path to the source image, the image you want to glitch.
- `output_filename` is the name you want to save the new image as. Be sure to include the file extension!
- `-o` signifies the path to the directory where you want to save the new image. This argument is optional. If you don't include it, `glitcher.py` uses the current working directory, that is, the directory `glitcher.py` is in.
- `-m` signifies how many times you want to mutate the image--that is, how many times you want `glitcher.py` to alter the base image. The higher the number, the more destroyed the image becomes. This is an optional argument; the default value is `25`.
- `-r` signifies how many pixels you want to replace each time the program mutates the image. By default, this value is `0`, meaning that it will replace every pixel with the new value each pass. The higher your image's resolution, the higher this number will have to be before you'll notice a difference. Of course, because pixels are replaced from the top-left, across to the top-right, then down to the next row of pixels at the left, you'll be leaving portions of the image untouched this way. Maybe that's what you want!
- `-f` signifies how many frames you want to include in an animated .GIF file made from the altered source image. This argument is optional and by default is `1`; in this case, `glitcher.py` doesn't make a .GIF file.
- `-k` signifies that you want to keep the individual pictures used to make an animated .GIF file. It doesn't take any arguments; just include `-k` and you'll keep the images.

So, for example:

```
glitcher.py C:\Users\User\Desktop\source.jpg transformed.jpg -o C:\Users\User\Desktop\ -m 50 -r 100
```

`glitcher.py` is unhelpful, and it won't tell you if you're going to try to replace a file that already exists. If you do something wrong, you'll get a Python error. It doesn't even set an upper limit on the number of passes. Go wild.

## Dependencies

`glitcher.py` relies on Pillow. Again, use `pip install Pillow` to add it to your system.

You'll also need `pyvips`, so you'll need `libvips`. It's beyond the scope of this README to tell you how to get that set up, so be sure to check the respective tools' documentation.

## Acquisition

Why would you bother to clone this? This should be on PyPI or whatever, but it's not because it's embarrassing. Just copy the contents of `glitcher.py`.