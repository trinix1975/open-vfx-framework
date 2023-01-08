"""
Utilities to manage anything related to a path.

Eg. Sequence of files
    File and directory editing/navigation
"""

import os
import re
import glob
import shutil

class Path(object):

    def __init__(self, path):

        self.set_path(path)

    def __repr__(self):
        cl = self.__class__
        if self.exists():
            status = 'existing'
        else:
            status = 'non existing'
        result = '<{}.{} object from {} {} at {}>'.format(cl.__module__, cl.__name__, status, self.__path, hex(id(self)))
        return result

    @staticmethod
    def format_size(size, decimal_number=1):
        for unit in ['B','KiB','MiB','GiB','TiB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return '{size:.{prec}f}{unit}'.format(size=size, prec=decimal_number, unit=unit)

    def path(self):
        return self.__path

    def set_path(self, path):

        if not path:
            self.__path = 'Undefined_Path'
        else:
            if path[-1] == '/': # remove the last / to unify the syntax internally
                path = path[:-1]
            self.__path = path

    def exists(self):
        """
        Return whether or not this path exists
        """
        return os.path.exists(self.__path)

    def is_file(self):
        """
        Return whether the path is a file
        """
        if not self.exists(): # We need to be sure the path exists.
            raise OSError('The following path does not exist. {}'.format(self.__path))
        result = False
        if os.path.isfile(self.__path):
            result = True
        return result

    def is_dir(self):
        """
        Return whether the path is a directory
        """
        if not self.exists(): # We need to be sure the path exists.
            raise OSError('The following path does not exist. {}'.format(self.__path))
        result = False
        if os.path.isdir(self.__path):
            result = True
        return result

    def parent(self, level=1):
        """
        Return a parent of the current path as a Path object

        Args:
            level  : The number of level where the parent is.
                        Example: 2 would be 2 parents above
        """
        if level < 2: # 1
            return Path(os.path.dirname(self.__path))
        else:
            level = level - 1
            parent = self.parent(level)
            return Path(parent.path()).parent()

    def directory(self):
        """
        Return the first parent directory if this is a file path.
        Return the current directory if this is already a directory.
        """
        if self.is_file():
            return self.parent()
        else:
            return self

    def create_folder(self):
        """
        Create a folder of the current paths. Create ancestor paths if needed.
        """
        if self.exists():
            if self.is_file():
                raise OSError('Cannot create a folder. A file already exists with the following path. {}'.format(self.__path))
        else:
            os.makedirs(self.__path)

    def size(self, human_readable=True, decimal_number=1):
        if self.is_file():
            size = os.stat(self.__path).st_size
            if human_readable:
                size = self.format_size(size, decimal_number=decimal_number)
            return size

    def list(self):
        if self.is_dir():
            return [Path('{}/{}'.format(self.__path, p)) for p in os.listdir(self.__path)]

    def name(self):
        """
        Return the path's last component. This is the file or directory name based on what type the path is
        """
        if self.exists():
            return os.path.basename(self.__path)

class Seq(object):

    def __init__(self, path):
        """
        Treat an file sequence as a whole in order to retrieve information from it
        or to manipulate the individual element of the sequence

        Files are considered part of a common sequence if they have the same
        naming except the frame number representing the sequence.

        path: Can be any of the following:
            -A single file name of an existing file like:
                /rootFolder/someOtherFolder/fileName.1.jpg

                /rootFolder/someOtherFolder/fileName.0001.jpg

                /rootFolder/someOtherFolder/fileName.1001.jpg

            -A formated sequence representation of existing files like:
                /rootFolder/someOtherFolder/fileName.%d.jpg

                /rootFolder/someOtherFolder/fileName.%04d.jpg

                /rootFolder/someOtherFolder/fileName.$F4.jpg

                /rootFolder/someOtherFolder/fileName.%FF.jpg
        """
        self.set_path(path)

    def __repr__(self):
        cl = self.__class__
        result = '<{}.{} object from {} at {}>'.format(cl.__module__, cl.__name__, self.path(format='*'), hex(id(self)))
        return result


    def set_path(self, path):

        pre_group = '(.+?)' # Any single character or more ending with a .
        post_group = '(\.[^0-9]+)$' # A . followed by a single or more non digit characters until the end
        frame_group = '(\.%[0-9]*d)' # Try the %04d %d %02d etc syntax
        match = re.search('{}{}{}'.format(pre_group, frame_group, post_group), path)
        if not match:
            frame_group = '(\.\$F+[0-9]*)' # Try the $F, $FF or $F4 etc syntax
            match = re.search('{}{}{}'.format(pre_group, frame_group, post_group), path)
            if not match:
                frame_group = '(\.[\*]+)' # Try the .*.
                match = re.search('{}{}{}'.format(pre_group, frame_group, post_group), path)
                if not match:
                    frame_group = '(\.[#]+)' # Try the .####.
                    match = re.search('{}{}{}'.format(pre_group, frame_group, post_group), path)
                    if not match:
                        frame_group = '(\.[.0-9]+)' # Try the .1001. any digits
                        match = re.search('{}{}{}'.format(pre_group, frame_group, post_group), path)

        if match: # This is a valid sequence
            self.__is_seq = True
            self.__pre_frame = match.group(1) + '.' # add the . back that we made part of the frame number
            self.__post_frame = match.group(3)
        else: # A single file without frame
            self.__is_seq = False

        self.__raw_path = path
        self.__valid_list = False # Reset the internal list status to tell it needs to requery the file system

    def path(self, format='%04d', frame=None, include_range=False, range_format=' ({}-{})', force_refresh=False):
        """
        Return the path according to the specified format.

        Args:
            format:              This string is inserted where the frames are.
                                 It can therefore be anything. Eg. ####, $F4, XXXX when frame is None.
                                 Otherwise it has to be a valid %d syntax. Eg. %04d, %02d.
            frame:               When provided the result is this frame number formated to the format parameter.
            include_range:       Shows the frame range at the end of the path.
            range_format:        Format to use when showing the range with include_range.
                                 Each curly brace is replaced with the first and last frame.
                                     Example: '[ {} to {} ]' -> '[ 1001 to 1200 ]'
            force_refresh:       Query the file system to get an updated view of the actual files.
                                 Otherwise the state of the file list matches what they
                                 were when the Path was first initialized.

        Returns:
            This is a description of what is returned.

        Raises:
            TypeError :          When we want to output a frame in particular but we don't provide
                                 a valid format with the %d syntax like %04d.

        Examples:
            import ovfx.path
            path = ovfx.path.Path('/path/to/somewhere/file.10.exr')
            path.path(format='####', include_range=True, range_format=' [{}-{}]')
            >>>/path/to/somewhere/file.####.exr [10-20]
        """

        if not self.__is_seq:
            result = self.__raw_path
        else:
            if frame: # Ouput the path with the frame in it
                try:
                    formated_frame = (format % frame)
                except TypeError: # This means the format didn't have any effect
                    raise TypeError(format + ' is not a valid format for outputing a frame number. Format must be with the %d syntax.')
                result = (self.__pre_frame + (format % frame) + self.__post_frame)
            else: # Output the path as a sequence format
                result = '%s%s%s' % (self.__pre_frame, format, self.__post_frame)
            if include_range:
                if self.count(force_refresh):
                    info = range_format.format(self.first_frame(), self.last_frame())
                else:
                    info = ' (No files)'
                result += info
        return result

    def is_seq(self):
        return self.__is_seq

    def __build_list(self, force_refresh=False):
        """
        Rebuild the file list from the file system based on the pre and post file segments
        """
        if not self.__valid_list or force_refresh: # Only do the following if the list needs to be rebuilt
            if not self.__is_seq:
                self.__file_list = glob.glob(self.__raw_path)
            else:
                self.__file_list = glob.glob('%s*%s' % (self.__pre_frame, self.__post_frame) )
                self.__file_list.sort()
                # Loop through files and filter out the ones without a numerical frame
                filtered_list = []
                for f in self.__file_list:
                    frame = f.replace(self.__pre_frame, '').replace(self.__post_frame, '')
                    filtered_list.append(f)
                self.__file_list = filtered_list
            self.__valid_list = True # Set the status back to a valid list

    def files(self, force_refresh=False):
        """
        Return all filenames
        """
        self.__build_list(force_refresh)
        return self.__file_list

    def count(self, force_refresh=False):
        """
        Return the number of files
        """
        self.__build_list(force_refresh)
        return len(self.__file_list)

    def frames(self, force_refresh=False):
        """
        Return the file frames found in the sequence
        """
        # if force_refresh:
        self.__build_list(force_refresh)
        result = []
        if self.__is_seq:
            if len(self.__file_list):
                for f in self.__file_list:
                    frame = f.replace(self.__pre_frame, '').replace(self.__post_frame, '')
                    # frame = int(frame)
                    result.append(frame)
            result.sort()

        return result

    def first_frame(self, force_refresh=False):
        """
        Return the sequence index from the first file in the sequence
        """
        frames = self.frames(force_refresh)
        if frames:
            return frames[0]

    def last_frame(self, force_refresh=False):
        """
        Return the sequence index from the last file in the sequence
        """
        # We need to get all the frames first because looking directly self.__file_list
        # will return .9.ext as a higher frame than .10.ext
        frames = self.frames(force_refresh)
        if frames:
            return frames[-1]

    def frame_range(self, force_refresh=False):
        """
        Return the sequence index from the first and last file in the sequence
        """
        frames = self.frames(force_refresh)
        if frames:
            return (frames[0], frames[-1])

    def size(self, human_readable=True, decimal_number=1):
        accum_size = 0
        for file in self.files():
            accum_size += os.stat(file).st_size
        if human_readable:
            accum_size = Path.format_size(accum_size, decimal_number=decimal_number)
        return accum_size

# def copy_file(source, destination):
#     """
#     Copy a file using the shutil.copyfile but create intermediate
#     directories if they don't already exist.
#     """
#     if not os.path.exists(os.path.dirname(destination)):
#         try:
#             os.makedirs(os.path.dirname(destination))
#         except OSError as exc: # Guard against race condition
#             if exc.errno != errno.EEXIST:
#                 raise
#     shutil.copyfile(source, destination)
#
# def open_file_browser(path, browser='nautilus'):
#     """
#     Open the specified file browser from a shell command at the location of path.
#     If path is a file, open at the parent directory location
#     """
#     open_location = ''
#     if os.path.isdir(path):
#         open_location = path
#     if os.path.isfile(path):
#         open_location = os.path.dirname(path)
#     if open_location:
#         os.system('{} {}'.format(browser, open_location))
#
# def convert_to_pyc(path):
#     """Return the path to .pyc if it's a .py that doesn't exist"""
#     if os.path.exists(os.path.expandvars(path)): # The expandvars is to get the real path instead of $AX_ACTIVE_REPO for example.
#         return path
#     else:
#         return path.replace('.py', '.pyc')
