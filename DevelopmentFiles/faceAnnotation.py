#!/usr/bin/env python3

### This script recognizes the face in the camera and creates a bounding box around the face.

'''Display a GUI window showing an annotated camera view.

Note:
    This example requires Python to have Tkinter installed to display the GUI.

This example uses tkinter to display the annotated camera feed on the screen
and adds a couple of custom annotations of its own using two different methods.
'''

import asyncio
import sys
import time

from PIL import ImageDraw

import anki_vector
from anki_vector import annotate


# Define an annotator using the annotator decorator
@annotate.annotator
def clock(image, scale, annotator=None, world=None, **kw):
    d = ImageDraw.Draw(image)
    bounds = (0, 0, image.width, image.height)

# Define a new annotator by inheriting the base annotator class
class Battery(annotate.Annotator):
    def __init__(self, img_annotator, box_color=None):
        super().__init__(img_annotator)
        self.battery_state = None
        self.battery_state_task = None
        if box_color is not None:
            self.box_color = box_color

    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)

        if not self.battery_state_task:
            self.battery_state_task = self.world.robot.get_battery_state()

        if asyncio.isfuture(self.battery_state_task) and self.battery_state_task.done():
            self.battery_state = self.battery_state_task.result()
            self.battery_state_task = self.world.robot.get_battery_state()

        if self.battery_state:
            batt = self.battery_state.battery_volts
            text = annotate.ImageText(f"BATT {batt:.1f}v", color="green", outline_color="black")
            # text.render(d, bounds)
            print(text)



def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial, show_viewer=True, enable_face_detection=True) as robot:
        robot.camera.image_annotator.add_annotator("battery", Battery)
        try:
            # Shutdown the program after 30 seconds
            time.sleep(300)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
