import os
import sys
import yaml


def config_yaml():
    """Returns config yaml path.
    First priority given to passed 0th argument.
    Second priority given to env var 'GMAIL_HELPER_CONFIG' value.

    Args: None
    """
    try:
        if os.path.exists(sys.argv[1]):
            return sys.argv[1]
        else:
            return "config.yaml"
    except:
        try:
            return os.environ("GMAIL_HELPER_CONFIG")
        except:
            return "config.yaml"


CONFIG = {}
try:
    with open(config_yaml(), "r") as ymlfile:
        CONFIG = yaml.load(ymlfile)
except:
    print("error reading config file: '%s'; would try env var as default else make error exit" % (config_yaml()))


def env_else_yaml(config_name):
    """Returns config value of provided name.
    First priority given to env var value for it.
    Second priority given to config yaml value for it.
    Else it prints error and exits.

    Args: None
    """
    try:
        envvar_name = "GMAIL_HELPER_%s" % (config_name)
        return os.environ(envvar_name)
    except:
        try:
            return CONFIG[config_name]
        except:
            print("failed to get config: %s" % (config_name))
            sys.exit(1)


def gmail_credential_jsonpath():
    return env_else_yaml("gmail_credential_jsonpath")

def gmail_auth_picklepath():
    return env_else_yaml("gmail_auth_picklepath")

def log_debug():
    return env_else_yaml("log_debug")

def data_basepath():
    return env_else_yaml("data_basepath")

def scopes():
    ret_val = env_else_yaml("scopes")
    if isinstance(ret_val, list):
        return ret_val
    else:
        return ret_val.split(",")

def since_year():
    return int(env_else_yaml("since_year"))

def before_year():
    return int(env_else_yaml("before_year"))

def filters_to_delete():
    ret_val = env_else_yaml("filters_to_delete")
    if isinstance(ret_val, list):
        return ret_val
    else:
        return ret_val.split(",")

def message_ids_to_skip():
    ret_val = env_else_yaml("message_ids_to_skip")
    if isinstance(ret_val, list):
        return ret_val
    else:
        return ret_val.split(",")

def labels_to_skip():
    ret_val = env_else_yaml("labels_to_skip")
    if isinstance(ret_val, list):
        return ret_val
    else:
        return ret_val.split(",")
