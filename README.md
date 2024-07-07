# glitcher
Manipulates images to give them a pseudo-glitch effect. In a really unnecessary, dumb way.

Ensure that you have Pillow installed! If you can `import PIL` without getting an error, you're good. If you do get an error, use `pip install Pillow`.

Get started by accessing the script's location in your terminal, then enter the following command:

```
glitcher.py image_location output_location passes
```

- `image_location` is a path to the source image, the image you want to glitch.
- `output_location` is a path to the output image. This is where you'll name the output, so be sure to specify the file extension.
- `passes` is an optional argument. This tells the program how many times you want it to process the image, with the image getting more ruined the higher the number you specify. If you don't include an integer here, `glitcher.py` uses `25`.

So, for example:

```
glitcher.py C:\Users\User\Desktop\source.jpg C:\Users\User\Desktop\glitched_image.jpg 50
```

`glitcher.py` is unhelpful, and it won't tell you if you're going to try to replace a file that already exists. If you do something wrong, you'll get a Python error. It doesn't even set an upper limit on the number of passes. Go wild.

## Dependencies

`glitcher.py` relies on Pillow. Again, use `pip install Pillow` to add it to your system.

## Acquisition

Why would you bother to clone this? This should be on PyPI or whatever, but it's not because it's embarrassing. Just copy the contents of `glitcher.py`.