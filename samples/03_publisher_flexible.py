
"""
Demonstrate the concept of what a custom publisher could be if made directly from the framework.

A universal publisher could use an external configuration file to define the mappings below.
"""

import ovfx.loc

# Uncomment the different paths to see how it adapts to any location models it finds in the mapping
source_path = '/mnt/prod/projects/MyProject/_assets/vehicules/car/3D/houdini/render/fx_fire/v043/MyProject_vehicules_car_fx_fire_v043.1234.bgeo.sc'
# source_path = '/mnt/prod/projects/MyProject/E400/Seq_010/0010/3D/houdini/render/fx_fire/v043/MyProject_E400_Seq_010_0010_fx_fire_v043.1001.tif'
# source_path = '/mnt/prod/projects/MyProject/_assets/props/marble_table/3D/houdini/cache/geo/main/v007/MyProject_props_marble_table_mdl_main_v007.bgeo.sc'

mappings = [
    {'source': ['software', 'render', 'image', 'shot'], 'target': ['publish', 'render', 'image', 'shot']},
    {'source': ['software', 'render', 'image', 'asset'], 'target': ['publish', 'render', 'image', 'asset']},
    {'source': ['software', 'render', 'geo', 'shot'], 'target': ['publish', 'render', 'geo', 'shot']},
    {'source': ['software', 'render', 'geo', 'asset'], 'target': ['publish', 'render', 'geo', 'asset']}
]

context_found = False
for mapping in mappings:
    if not context_found:
        # Create a location object from the source location model
        source = ovfx.loc.Location(mapping['source'])
        # Try to extract the context.
        source.extract_frags(source_path)
        if source.valid():
            context_found = True
            # Create the target location object
            target = ovfx.loc.Location(mapping['target'])

if context_found:
    print(source.info())
    # Apply the source context to the target model to build the target path
    target_path = source.bundle.translate(target.model())

    print('Copying: {}'.format(source_path))
    print('To     : {}'.format(target_path))
else:
    print('Invalid context for path: {}'.format(source_path))
