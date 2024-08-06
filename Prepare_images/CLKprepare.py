from PIL import Image
import os
import argparse
import CLKImagePlugin

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='CLK Image Preparation',
        description='Convert single image or folder of images to CLK',
        epilog='Perfect to get your EleksTubeHax running')

    parser.add_argument('folder', metavar='F', type=str, help='Path to folder of images')
    parser.add_argument('-i',dest='prefix', type=str, default="", help='Prefix number for files when creating CLK')
    parser.add_argument('-s', dest="show", action='store_true' ,help="Program will instead show CLK file called out")
    args = parser.parse_args()

    if args.show:
        with Image.open(args.folder)as im:
            im.show()
    else:
        img_list = [img for img in os.listdir(args.folder) if not ".clk" in img]
        for img in img_list:
            im =Image.open(os.path.join(args.folder,img))
            img_name = im.fp.name.split(".")[0]+".clk"
            if args.prefix:
                img_name = img_name[:-5]+args.prefix+img_name[-5:]
            im.save(img_name)
