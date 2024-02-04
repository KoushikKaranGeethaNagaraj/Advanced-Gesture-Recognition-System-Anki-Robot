import threading
import time
import anki_vector
from anki_vector import events
from anki_vector.util import degrees
import cv2
import numpy as np
import os


import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        # You can find these sounds files here:
        # https://github.com/anki/vector-python-sdk/blob/master/examples/sounds/vector_alert.wav
        # https://github.com/anki/vector-python-sdk/blob/master/examples/sounds/vector_bell_whistle.wav
        #
        # Paste these two wav files next to this tutorial to play sounds.
        robot.audio.stream_wav_file("dead.wav", 95)



if __name__ == "__main__":
    main()

