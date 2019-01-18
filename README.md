# Camera-Line-Tracking
Python script that uses a camera to detect a line and generate info about it

This script was designed to take camera input and look at a dark line against a
light background. When it sees the line it isolates it with opencv color
thresholding. After this, it makes an opencv contour around it that should be a
rectangle.

With the contour it can get information about the line, like the angle it is
rotated. It should also be able to get the distance the center of the line is
from the center of the camera feed in inches, assuming a line that is two
inches thick, but it currently doesn't work accurately.

This script was originally made by Alejandro Ramos, Swanand Kanere, Matthew
Chen, and Jack Hankin for the 2019 season of the Bronx Science SciBorgs FRC
team. Hopefully it will be used, but even if it's not, we still learned a lot
about computer vision from the project.