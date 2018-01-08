from pyhocon import ConfigFactory


def load_config(file_path):
    """
    Wrapper over pyhocon that returns a python dict rather
    than pyhocon's structure, and also corrects None values
    :param file_path: path of the config file to parse
    :return: config dict
    """
    conf = ConfigFactory.parse_file(file_path)
    _load_config(conf)
    return dict(conf)


def _load_config(conf):
    """
    Recursive function that iterates over the structure returned
    by pyhocon's parser and corrects None values and transforms
    it into a Python dict
    :param conf: structure returned by pyhocon's parser
    :return: config dict
    """
    if isinstance(conf, list):
        for i in range(len(conf)):
            try:
                conf[i] = _load_config(conf[i])
                if not isinstance(conf[i], list):
                    conf[i] = dict(conf[i])
            except:
                conf[i] = conf[i]
    else:
        for key in conf:
            try:
                conf[key] = _load_config(conf[key])
                if not isinstance(conf[key], list) and not isinstance(conf[key], str):
                    conf[key] = dict(conf[key])
            except:
                conf[key] = conf[key]

    return conf
