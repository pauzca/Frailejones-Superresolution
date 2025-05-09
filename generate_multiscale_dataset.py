# codigo copiado de https://github.com/xinntao/Real-ESRGAN/tree/master
import argparse
import glob
import os
from PIL import Image


def main(args):
    # and the smallest image whose shortest edge is 400
    scale_list = [0.75, 0.4, 0.3]
    shortest_edge = 576
    path_list = sorted(glob.glob(os.path.join(args.input, '*')))
    print(path_list)
    for path in path_list:
        print(path)
        basename = os.path.splitext(os.path.basename(path))[0]

        img = Image.open(path)
        width, height = img.size
        for idx, scale in enumerate(scale_list):
            print(f'\t{scale:.2f}')
            rlt = img.resize((int(width * scale), int(height * scale)), resample=Image.LANCZOS)
            rlt.save(os.path.join(args.output, f'{basename}T{idx}.png'))

        # save the smallest image which the shortest edge is 400
        if width < height:
            ratio = height / width
            width = shortest_edge
            height = int(width * ratio)
        else:
            ratio = width / height
            height = shortest_edge
            width = int(height * ratio)
        rlt = img.resize((int(width), int(height)), resample=Image.LANCZOS)
        rlt.save(os.path.join(args.output, f'{basename}T{idx+1}.png'))

if __name__ == '__main__':
    """Generate multi-scale versions for GT images with LANCZOS resampling.
    It is now used for DF2K dataset (DIV2K + Flickr 2K)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='../dataset/19_dic_1cm/dataset/images/', help='Input folder')
    parser.add_argument('--output', type=str, default='../dataset/19_dic_1cm/multiscale', help='Output folder')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    main(args)
