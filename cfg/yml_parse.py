import yaml
import os


class AttrDict(dict):
    """
    If name in dict,then get the name of the dict. NOT USED
    """

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self[name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            self[name] = value


def parse_yaml(ymlfilename):
    """
    Convert the dict to be [cfg.Name...]
    :param ymlfilename:
    :return:
    e.g :
        yaml_cfg['PATH']['TMP_DIR']
    """
    with open(ymlfilename, 'r', encoding='UTF-8') as f:
        yaml_cfg = yaml.load(f, Loader=yaml.FullLoader)
        cfg = AttrDict(yaml_cfg)
        cfg.PATH = AttrDict(cfg.PATH)
        # change the relative root to the absolute root.
        # for k, path in cfg.PATH.items():
        #     path = os.path.join(real_path, path)
        #     cfg.PATH[k] = path

        cfg.TRAIN = AttrDict(cfg.TRAIN)
        cfg.TEST = AttrDict(cfg.TEST)
    return cfg

#
# global cfg
# cfg = parse_yaml('../../cfg/yolov2.yml')
