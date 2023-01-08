
import collections
import copy
import os
import re
import yaml

from ovfx import exceptions as ex
import importlib
import ovfx.cfg

class Location(object):

    def __init__(self, model):
        self.__config = ovfx.cfg.location
        self.set_model(model)
        self.__bundle = FragBundle()

    def __repr__(self):
        cl = self.__class__
        result = '<{}.{} object "Valid={}" at {}>'.format(cl.__module__, cl.__name__, self.valid(), hex(id(self)))
        return result

    def set_model(self, model):
        if type(model) == str: # Use the model directly
            self.__model = model
        else: # Use the settings from the config
            location = self.__config
            if type(model) == str: # Directly that key
                location = location[key]
            else: # Add go down one level for each key in the list
                for key in model:
                    location = location[key]
            self.__model = location

    def model(self):
        return self.__model

    def tags(self):
        """Return all tags from the current model"""
        result = []
        for match in re.finditer('<[a-z_]*>', self.__model):
            result.append(match.group()[1:-1])
        return result

    @property
    def bundle(self):
        return self.__bundle

    @bundle.setter
    def bundle(self, bundle):
        self.__bundle = bundle

    def frags(self):
        """
        Return fragments from the internal bundle.
        The fragments must match one of the model's tags.
        """
        return tuple([frag for frag in self.__bundle.frags() if frag.id() in self.tags()])

    def extract_frags(self, path, expand=False):
        # Clears out any fragment set from a previous extraction. Required when skipping already found fragments earlier in the path from the same extraction.
        self.__bundle.reset_frags()
        expanded_model = self.__model
        if expand:
            expanded_model = os.path.expandvars(expanded_model)

        exp = expanded_model
        complement = re.split('<[a-z_]*>', expanded_model)
        complement = [s.replace('.', '\.') for s in complement]  # The dot must be escaped because it's a special character in regex
        regex_list = []
        key_list = []
        for match in re.finditer('<[a-z_]*>', expanded_model):
            key = match.group()[1:-1]
            # Get the regex
            if key not in self.__bundle():
                raise ex.NotFound('The following path fragment definition cannot be found in the studio configuration file: {}'.format(key))
            key_list.append(key)
            # Extract the data
            regex_list.append(self.__bundle(key).regex())

        # Go through each tag one at a time and extract the value
        for i in range(len(regex_list)):
            key = key_list[i]
            regex_current_list = list(regex_list)
            regex_current_list[i] = '({})'.format(regex_list[i]) # Surround the current tag with () to make it the active group
            # Combine the regex with the complement list
            result = [None]*(len(complement)+len(regex_current_list))
            result[::2] = complement
            result[1::2] = regex_current_list
            exp = ''.join(result)
            result_match = re.match(exp, path)
            # Does not try to extract a tag when already found earlier in the path.
            # This helps avoiding tags that are often abiguous near the end of a path.
            # For example if the project name has an _ in it but each tag is also
            # separated by an _ in the file name, the regex may misinterpret the _ separator
            # with the actual _ in the project name. Extracting the project from the folder name
            # is not ambiguous because it's separated by slashes so _ can only be part of the name.
            #
            # However it means that it doesn't enforce consistency with a tag that occurs mutliple time.
            # For example if the project name folder is different than the one we see in the file name,
            # it will ignore the one in the file name without complaining.
            # We could add an optional validation that would error out if it detects discrepency between values for the same tags.
            if self.__bundle(key).value() == None:
                if result_match == None:
                    self.__bundle(key).set_value(None)
                else:
                    self.__bundle(key).set_value(result_match.groups()[0])

    def path(self, bundle=None, **kwargs):
        # Assign to a temp FragBundle object because might override some parameters
        if bundle: # Use the custom FragBundle object instead
            bundle_obj = bundle.duplicate()
        else: # Use the internal one
            bundle_obj = self.__bundle.duplicate()
        # override the value first and let it raise an error if the format is invalid
        bundle_obj.set_value(**kwargs)
        path = self.__model
        for tag in list(set(re.findall('<[a-z_]*>', path))):
            key = tag[1:-1]
            if key in bundle_obj(): # get the value from the var
                value = bundle_obj(key).value() if bundle_obj(key).value() is not None else 'UNDEFINED'
            path = path.replace(tag, value)
        return path

    def parent(self, id, index=0):

        result = []
        for match in re.finditer('<[a-z_]*>', self.__model):
            key = match.group()[1:-1]
            if key == id:
                span = match.span()
                result.append(self.__model[:span[1]])
        if not result:
            raise KeyError('The following fragment id cannot be found in the current location model: {}'.format(id))
        new_obj = copy.deepcopy(self)
        try:
            new_obj.set_model(result[index])
        except IndexError:
            raise IndexError('The index {} is outside the tag list "{}" of size {}.'.format(index, id, len(result)))
        return new_obj

    def valid(self):
        """
        Return whether there is a valid non Null internal fragment for each tag
        found in the path in the form of <tag>
        """
        result = True
        for tag in list(set(re.findall('<[a-z_]*>', self.__model))):
            key = tag[1:-1]
            if key not in self.__bundle() or self.__bundle(key).value() is None:
                result = False
        return result

    def info(self, include_empty=False):
        result = '##########{}##########'.format('#### Context ####' if self.valid() else ' Invalid Context ')
        result += self.__bundle.info(include_empty)
        result += '\n#####################################'
        return result

class Frag(object):
    """Fragment object representing a path variable component."""

    def __init__(self, id):
        frag = ovfx.cfg.fragment[id]
        self.__id = id
        self.__label = frag['label']
        self.__regex = frag['regex']
        self.__value = None

    def __repr__(self):
        cl = self.__class__
        result = '<{}.{} object "id={}, value={}" at {}>'.format(cl.__module__, cl.__name__, self.__id, self.__value, hex(id(self)))
        return result

    def __eq__(self, other):
        if type(other) == str: # compare with the id
            return self.__id == other
        elif type(self) == type(other):
            return id(self) == id(other)
        else:
            raise NotImplementedError

    def id(self):
        return self.__id

    def label(self):
        return self.__label

    def regex(self):
        return self.__regex

    def value(self):
        return self.__value

    def set_value(self, value):
        if not self.validate_value(value):
            raise ex.InvalidFormat('The following value for fragment "{}" does not comply with the regular expression \"{}\": {}'.format(self.__id, self.__regex, value))
        self.__value = value

    def validate_value(self, value):
        result = False
        if value is None or re.match('{}$'.format(self.__regex), value):
            result = True
        return result

    def duplicate(self):
        return copy.deepcopy(self)

class FragBundle(object):
    """Collection of fragments representing a context"""
    def __init__(self):
        self.__config = ovfx.cfg.fragment
        self.reset_frags()

    def __repr__(self):
        cl = self.__class__
        result = '<{}.{} object "Number of Frag={}" at {}>'.format(cl.__module__, cl.__name__, len(self.__frags), hex(id(self)))
        return result

    def __call__(self, id=None):
        if id:
            if id in self.__frags:
                return self.__frags[id]
        else:
            return [self.__frags[k] for k in self.__frags]

    def reset_frags(self):
        self.__frags = collections.OrderedDict()
        for key in self.__config:
            frag = Frag(key)
            self.__frags[key] = frag

    def frag(self, id):
        result = None
        if id in self.__frags:
            return self.__frags[id]

    def frags(self):
        return tuple(self.__frags.values())

    def set_value(self, **kwargs):
        for k in kwargs:
            if k not in self.__frags:
                raise ex.NotFound('Cannot find the following fragment: {}'.format(k))
            self.__frags[k].set_value(kwargs[k])

    def remove_frag(self, id):
        """Remove the frag from this bundle"""
        if id in self.__frags:
            self.__frags.pop(id)

    def _set_frags(self, frag_dict):
        self.__frags = frag_dict

    def duplicate(self):
        return copy.deepcopy(self)

    def translate(self, value):
        """
        Translate the "value" parameter to convert the tags <tag> with
        the internal value from the matching Frag
        """
        for tag in list(set(re.findall('<[a-z_]*>', value))):
            key = tag[1:-1]
            if key in self.__frags:
                if self.__frags[key].value() == None:
                    raise ValueError('The following frag does not have a value assigned to it: {}'.format(key))
                value = value.replace(tag, self.__frags[key].value())
        return value

    def info(self, include_empty=True):
        # Extract the labels and frag values
        labels, frags = zip(*[(self.__frags[key].label(), self.__frags[key]) for key in self.__frags])
        # Extract the values from the frags. Convert the None to a string representation
        values = [i.value() for i in frags]
        result = ''
        max_len = len(max(labels, key=lambda x: len(x)))
        for label, value in zip(labels, values):
            if value != None or include_empty:
                result += '\n{}{}: {}'.format(' ' * (max_len - len(label)), label, value)
        return result

    # def same_values(self, other):
    #     """
    #     Compare this object with another one and return True if they have the
    #     same number of Frag with the same id and same value
    #     """
    #     if len(self.frags()) != len(other.frags()): # not the same amount of Frags
    #         return False
    #     else:
    #         for frag in self.frags():
    #             if frag.id() not in other.frags(): # it's missing the Frag
    #                 return False
    #             elif frag.value() != other(frag.id()).value(): # not the same value
    #                 return False
    #     return True
