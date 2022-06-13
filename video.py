from re import I
from click import command
from halib import filesys
import os
from numpy import source
from tqdm import tqdm


from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(
        description="Help")
    parser.add_argument('-source', '--source', type=str,
                        help='video file or video folders', default='some_string')
    parser.add_argument('-weights', '--weights', type=str,
                        help='model weight')
    parser.add_argument('-conf', '--conf', type=float,
                        help='confidence threshold', default=0.5)
    return parser.parse_args()


def main():
    args = parse_args()
    source = args.source
    weights = args.weights
    conf = args.conf

    video_files = None
    if filesys.is_file(source):
        print('Processing file: {}'.format(source))
        video_files = [source]
    elif filesys.is_directory(source):
        # test_video_dir = './data/mobility_test_video'
        test_video_dir = source
        video_files = filesys.filter_files_by_extension(test_video_dir, '.mp4', recursive=False)

        if len(video_files) > 0:
            for _, video_file in enumerate(tqdm(video_files)):
                print(video_file)
                command = f"python detect.py --weights {weights} --img 640 --conf {conf} --source {video_file}"
                os.system(command=command)
        else:
            print('No video files found in {}'.format(test_video_dir))

    else:
        print("Source is not a file or directory")


if __name__ == "__main__":
    main()
