# Installation

## Prerequisites
OpenVFX needs the [yaml](https://pyyaml.org/wiki/PyYAMLDocumentation) library installed. Make sure the yaml package parent directory is included in the PYTHONPATH.

## ovfx Python Package
The included ovfx python package needs to be copied to a location that is included in the PYTHONPATH.

## Config Files
You need to create the two following configuration files.

    fragment.yaml
    location.yaml
    
Those files must exist in a folder that is set to the variable OVFX_CONFIG_DIR. For consistency it is better to call this folder **config**.
    
Example:

    $HOME/open_vfx_site/config/fragment.yaml
    $HOME/open_vfx_site/config/location.yaml

    OVFX_CONFIG_DIR=$HOME/open_vfx_site/config
    
# Configuration
You can look at the [samples](./samples) folder that comes with the code to better understand the roles of the configuration files from the Python script examples. Here is the basic information to explain what needs to be configured.

## Location
The location.yaml config file contains a location model for each path type needed by the tools.

A model is just like a regular path but it includes tags where a variable amount of folder can exist at that position. The tags are surrounded by <>

```
scene: /prod/projects/<proj>/<epis>/<seq>/<shot>/<task>/work/houdini/hip/<epis>_<seq>_<shot>_<task>_<scenedesc>_v<ver>.hip
```

Note that you can define a model inside a hierarchy to better organize them by category. In that case it would look like the following

```
houdini:
   scene:
      shot: /prod/projects/<proj>/<epis>/<seq>/<shot>/<task>/work/houdini/hip/<epis>_<seq>_<shot>_<task>_<scenedesc>_v<ver>.hip
```

## Fragment
The fragment.yaml config file contains a unique fragment definition for all potential fragments (tags) used by the location models. A fragment entry must include its code name, a label and a regular expression.

```
proj:
  label: Project
  regex: '[a-zA-Z0-9_]+'
```

The code name is the identifier we refer to when used in a path as a tag.

The label is the full name of that fragment.

The regular expression is what the internal **re** regular expression Python module uses to determine whether the path will match or not the tag. Here are a few examples of what those expressions can be.

**Include one or more alphabetical characters**

    [a-zA-Z]+
    
**Include one or more alphanumerical characters**

    [a-zA-Z0-9]+
    
**Include one or more alphanumerical or underscore characters**
    
    [a-zA-Z0-9_]+
