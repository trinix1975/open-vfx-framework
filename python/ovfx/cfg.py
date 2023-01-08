
import os
import yaml

# from ovfx import exceptions as ex

def config(name):
    """
    Get the content of the setup configuration file.

    The config files are all in the same standard location.

    Args:
        name     : Name of the file without the .yaml extension

    Examples:
        import ovfx.cfg
        loc = ovfx.cfg.config('location')
    """

    config_path = '{}/{}.yaml'.format(os.getenv('OVFX_CONFIG_DIR'), name)
    if not os.path.exists(config_path):
        raise IOError('The following configuration file does not exist: {} Make sure the OVFX_CONFIG_DIR variable is set.'.format(config_path))
    with open(config_path) as f:
        # Used to be the following but when existing yaml library are too old it errors out
        # data = yaml.load(f, Loader=yaml.FullLoader)
        data = yaml.safe_load(f)
    return data

fragment = config('fragment')
location = config('location')
