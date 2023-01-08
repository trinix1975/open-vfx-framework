"""
Demonstrates how we could implement an HDRI browser that shows thumbnails of all
images found based on drop down menu selection.

The drop down menus would be filled dynamically using the same location model.

An image browswer could be generalized to any sort of images or sequences
like an element library. As long as we provide a configuration mechanism that allows
multiple kind of images location, the universal image browser could give access to them all.
"""
import ovfx.loc

# Result of what the user would pick in the drop down menus.
project = 'MyProject'
epis = 'E300'
seq = '010'
hdricat = 'car' # If the user wants only HDRIs from the car category
hdricat = '*' # If the user wants all HDRIs regardless of the category

# Create the location object
hdri = ovfx.loc.Location(['hdri'])
# Set the corresponding fragments for each value in the drop down menus.
hdri.bundle.frag('proj').set_value(project)
hdri.bundle.frag('epis').set_value(epis)
hdri.bundle.frag('seq').set_value(seq)
hdri.bundle.frag('hdricat').set_value(hdricat)
print(hdri.info())
print('')

# Apply the current context on the current location model to build the search path
path = hdri.bundle.translate(hdri.model())
print('Path used for a glob search: {}'.format(path))
