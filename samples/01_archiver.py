"""
The simplest use of the framework.

It takes a path as a source, extract the context from a location model that
is defined directly at the first level of the location.yaml configuration file
and output another path from another location model.
"""
import ovfx.loc

# A simple path
source_path = '/mnt/prod/projects/MyProject'
# But it doesn't matter if the path has more information than the model needs.
# It is simply ignored by the context extraction process.
source_path = '/mnt/prod/projects/MyProject/seq_X/shot_Y/etc'
# Uncomment the following line to test how it extracts a different project name
# source_path = '/mnt/prod/projects/SecondProject'

# Create a location object from the "project" location model
source = ovfx.loc.Location(['project'])
print('The source location model is: {}'.format(source.model()))

# Extract the context from a path that matches the internal model "project"
print('Extracting project from the source path')
source.extract_frags(source_path)
print(source.info())
print('')

# Create a location object that uses the "project_archive" model
target = ovfx.loc.Location(['project_archive'])
print('The target location model is: {}'.format(target.model()))
# Use the translate function from the location object that owns the context.
# All tags in the path will be translated to their corresponding fragment value
target_path = source.bundle.translate(target.model())
print('The source path is: {}'.format(source_path))
print('The target path is: {}'.format(target_path))
