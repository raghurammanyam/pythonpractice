import os
import os.path
from PIL import Image
work_dir =os.get_cwd()
def imgstich():

    try:
        empty=[]
        image_dir = os.path.abspath("/home/caratred/Downloads/combine")
        print(image_dir)
        # list all files in directory
        files = os.listdir(image_dir)
        print(files)
        # # get all PNGs
        # png_files = filter(lambda x: x.endswith(".jpeg"), files)
        # # make file paths absolute
        # print(png_files,".....///")
        # image_files = map(lambda x: os.sep.join([image_dir, x]),files)
        for x in files:
            empty.append(os.sep.join([image_dir,x]))

        print(empty,",,,,,,")

        n_files = len(empty)
        # print (n_files)

        target_img = None
        n_targets = 0
        collage_saved = False
        for n in range(n_files):
            print("looop")
            img = Image.open(empty[n])
            img.thumbnail((700, 300))

            if n % 64 == 0:
                # create an empty image for a collage
                target_img = Image.new("RGB", (800, 800))
                n_targets += 1
                collage_saved = False

            # paste the image at the correct position
            i = int(n / 8)
            j = n % 8
            target_img.paste(img, (100*i, 100*j))

            if (n + 1) % 64 == 0 and target_img is not None:
                # save a finished 8x8 collage
                target_img.save("/home/caratred/{0:04}.jpeg".format(n_targets))
                collage_saved = True
                print(",,,")

        # save the last collage
        if not collage_saved:
            target_img.save("/home/caratred/{0:04}.jpeg".format(n_targets))
            print("..,,,,")
    except:
        print("notok")
imgstich()
