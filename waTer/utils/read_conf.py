# -*- coding: utf-8 -*-
import toml


def get_conf(conf_file_path):
    """read toml conf file for latter use.
    :param conf_file_path: absolute path of conf file.
    :return:a dict contains configured infomation.
    """
    with open(conf_file_path) as conf_file:
        config = toml.loads(conf_file.read())
    return config