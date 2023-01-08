
"""
Demonstrate how we can translate one path to another using the framework.
Note how the publish folder doesn't have the same structure as the source.
Even the published file name is different although it uses the same context fragments.
"""

import ovfx.loc

# With a frame number
source_path = '/mnt/prod/projects/MyProject/E400/Seq_010/0010/3D/houdini/render/fx_fire/v043/MyProject_E400_Seq_010_0010_fx_fire_v043.1001.tif'
# Single frame without a number
# source_path = '/mnt/prod/projects/MyProject/E400/Seq_010/0010/3D/houdini/render/fx_fire/v043/MyProject_E400_Seq_010_0010_fx_fire_v043.tif'
# A different shot
# source_path = '/mnt/prod/projects/BetterProject/120/080/0020/3D/maya/render/lgt_table/v003/BetterProject_120_080_0020_lgt_table_v003.1012.exr'

# Create a location object from the houdini shot image render location model
source = ovfx.loc.Location(['software', 'render', 'image', 'shot'])
# Extract the context.
source.extract_frags(source_path)

# Output the info
print(source.info())
# Create the target location object
target = ovfx.loc.Location(['publish', 'render', 'image', 'shot'])
# Apply the source context to the target model to build the target path
target_path = source.bundle.translate(target.model())

print('Copying: {}'.format(source_path))
print('To     : {}'.format(target_path))
