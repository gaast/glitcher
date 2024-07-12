import argparse
import binascii
import os
from PIL import Image
import pyvips
import random
import re

# Set up the constants.
VALUES = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0a", "0b", "0c", "0d", "0e", "0f",
          "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1a", "1b", "1c", "1d", "1e", "1f",
          "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2a", "2b", "2c", "2d", "2e", "2f",
          "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3a", "3b", "3c", "3d", "3e", "3f",
          "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4a", "4b", "4c", "4d", "4e", "4f",
          "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5a", "5b", "5c", "5d", "5e", "5f",
          "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6a", "6b", "6c", "6d", "6e", "6f",
          "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7a", "7b", "7c", "7d", "7e", "7f",
          "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "8a", "8b", "8c", "8d", "8e", "8f",
          "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "9a", "9b", "9c", "9d", "9e", "9f",
          "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "aa", "ab", "ac", "ad", "ae", "af",
          "b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "ba", "bb", "bc", "bd", "be", "bf",
          "c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb", "cc", "cd", "ce", "cf",
          "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "da", "db", "db", "dd", "de", "df",
          "e0", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "ea", "eb", "ec", "ed", "ee", "ef",
          "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "fa", "fb", "fc", "fd", "fe", "ff"]

def glitch(input, output, dest, passes, max_replacements, frames, delete=True):
    # Get the image data.
    with Image.open(input) as img:
        img_bytes = img.tobytes()
        # Can't forget to grab the dimensions.
        w = img.width
        h = img.height
        hex_data = binascii.hexlify(img_bytes).decode()

    images = []

    # Start the processing loop.
    for frame in range(frames):
        modified_data = ""
        frame_images = []
        for i in range(passes):
            # Get the regex and the replacement.
            r = f"{random.choice(VALUES)}"
            repl = random.choice(VALUES)
            
            # If the replacement is the same as the pattern, reroll the replacement. If they're the same again,
            # well, who cares. Because, like. Damn.
            if r == repl:
                repl = random.choice(VALUES)

            # Modify the data.
            if modified_data == "":
                modified_data = re.sub(r, repl, hex_data, max_replacements)
            else:
                modified_data = re.sub(r, repl, modified_data, max_replacements)

        # Convert the hex back to binary, then save the image.
        converted_data = binascii.unhexlify(modified_data)

        new_img = Image.frombytes("RGB", (w, h), converted_data)

        if frames == 1:
            new_img.save(os.path.join(dest, output))
        else:
            name = output.split(".")[0]
            ext = output.split(".")[1]
            new_img.save(os.path.join(dest, name + str(frame) + "." + ext))
            frame_images.append(os.path.join(dest, name + str(frame) + "." + ext))
            images.append(new_img)

    images = [pyvips.Image.new_from_file(os.path.join(dest, name + str(i) + "." + ext)) for i in range(len(images))]

    if frames > 1:
        roll = pyvips.Image.arrayjoin(images, across=1)

        roll = roll.copy()
        roll.set_type(pyvips.GValue.array_int_type, "delay", [99] * len(images))
        roll.set_type(pyvips.GValue.gint_type, "page-height", images[0].height)

        roll.write_to_file(os.path.join(dest, name + ".gif"))

        if delete:
            for frame_image in frame_images:
                os.remove(frame_image)

if __name__ == "__main__":
    # Give this program a .JPG image and some parameters, and it'll "glitch" the image's pixel values
    # by converting it to hex, doing some replacements, then converting it back to binary. It's a shame
    # that converting between formats isn't lossy! But, oh well.

    args = None

    parser = argparse.ArgumentParser(description="A program to add pseudoglitch effects to images.")
    parser.add_argument("filename", help="The source file's path.", nargs=1)
    parser.add_argument("output_filename", help="The base name for the output file.", nargs=1)
    parser.add_argument("-o", "--output_dest", help="The output destination directory; if you don't include this, glitcher.py uses the current working directory.", nargs=1, default=os.getcwd())
    parser.add_argument("-m", "--mutations", help="The number of times to edit pixel data per pass.", default=25, nargs=1, type=int)
    parser.add_argument("-r", "--replacements", help="The number of pixel values to replace per mutation.", default=0, nargs=1, type=int)
    parser.add_argument("-f", "--frames", help="The number of frames to include in GIF output. Include a number here to create a .GIF; each frame is a new image generated.", default=1, nargs=1, type=int)
    parser.add_argument("-k", "--keep", help="Include this flag to keep all of the images used to make a .GIF.", action="store_false")
    args = parser.parse_args()

    img_file = args.filename[0].strip()
    output_name = args.output_filename[0].strip()
    output_dest = args.output_dest[0].strip()
    mutations = args.mutations[0]
    try:
        replacements = args.replacements[0]
    except:
        replacements = args.replacements
    try:
        frames = args.frames[0]
    except:
        frames = args.frames
    # This keeps the frames when it's FALSE. I know this is stupid.
    keep_frames = args.keep

    glitch(img_file, output_name, output_dest, mutations, replacements, frames, keep_frames)
