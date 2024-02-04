# Anki-Robot-Advanced-Gesture-Recognition-System<br>
Face-to-Robot Interaction with Anki Vector to Support Wellness and Mental Health<br>

Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices. Someone experiencing mental health problems could have their thinking, mood, and behavior affected. Some of the benefits of positive mental health include:<br>
● Coping with life’s stresses<br>
● Being productive and positively contributing to the community<be>

There are several ways to maintain positive mental health including:<br>
● Connecting with others<br>
● Staying positive<br>
● Getting physically active<be>

Robot interaction with Anki Vector refers to making facial expressions (happy, sad, Neutral, Angry, and Disgusted) to the robot.<br>

You can understand the project better by reading AnkiRobotGestureRecognitionFinalReport.pdf and referring to AnkiRobotGestureRecognitionPresentation.pdf.<br>


This repository hosts a comprehensive solution for integrating advanced face and gesture detection capabilities with the Anki Vector robot, aimed at enhancing user mood through interactive tasks and actions. Despite the abundance of research in the fields of face and gesture recognition, their practical application in robotics has often been challenging. Our work successfully bridges this gap, offering a streamlined approach for empowering the Anki Vector robot with these sophisticated functionalities.<br>

The code within this repository is the result of meticulous development, enabling the robot to not only recognize facial expressions and gestures but also to respond in ways that positively influence the user's mood. Beyond interaction, the project extends into analytical realms, employing data gathered during interactions to predict the effectiveness of the Anki Vector robot in mood alteration. This analytical phase offers valuable insights into the robot's impact on users, showcasing its potential as a tool for mood enhancement and emotional well-being.<br>

To give an overview of the project:<br>
● The anki-vector-robot is set up and connected to the phone initially then a PC and it is Linux-based(recommended for development). This repository does not include the necessary setup for that as there are other plenty of resources (https://github.com/anki/vector-python-sdk).<br>

● Upon establishing a connection with a PC, the Anki Vector robot becomes programmable, allowing for access, control, and customization of its code, albeit the process requires a nuanced approach. This project focuses on leveraging the Anki Vector robot's camera to identify and capture facial expressions. The subsequent steps involve cropping the captured facial data for further processing. The refined image is then analyzed using a model trained on the Real-world Affective Faces Database (RAF-DB), a robust dataset designed for emotion recognition. This enables the Anki Vector robot to interpret human emotions with a high degree of accuracy. In addition to utilizing its built-in gesture detection capabilities, the modified code offers the flexibility to switch to the external model for enhanced emotion recognition. This dual-mode functionality not only broadens the robot's interactive capabilities but also enriches the user experience by responding to emotional cues more effectively.<be>

Note: Given the Anki Vector robot's limited computational capacity, all preprocessing tasks are executed on the connected PC. Subsequently, the robot receives commands from the PC to execute specific actions based on the processed data, ensuring efficient operation and interaction without overburdening the robot's onboard processor.<be>




