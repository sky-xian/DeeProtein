"""
DeeProtein model.
Run it. Run it. Run it.
"""

import controller as cont
import logging
import argparse
import json
import os
import sys


def set_default_options(config_file, parser):
    """
    Read the config.JSON and set the default options accordingly.
    :return:
    """
    with open(config_file, 'r') as open_config_file:
        config_dict = json.load(open_config_file)

    # define a mapping from string to callable type:
    str2type = {'str': str,
                'int': int,
                'float': float}

    for arg in config_dict.keys():
        if config_dict[arg]['short']:
            parser.add_argument(arg, config_dict[arg]['short'],
                                default=config_dict[arg]['value'],
                                help=config_dict[arg]['help'],
                                type=str2type[config_dict[arg]['type']],
                                )
        else:
            parser.add_argument(arg,
                                default=config_dict[arg]['value'],
                                help=config_dict[arg]['help'],
                                type=str2type[config_dict[arg]['type']],
                                )


def set_up_logger(info_path, name):
    """
    Set up the loggers for the module. Also set up filehandlers and streamhandlers (to console).
    """
    # get a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    os.makedirs(info_path, exist_ok=True)
    fh = logging.FileHandler(os.path.join(info_path, '{}.log'.format(name)))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def main():
    # Define the options for DeeProtein
    parser = argparse.ArgumentParser(description='Options to run DeeProtein')
    set_default_options(config_file=os.path.join(sys.path[0], 'config.JSON'), parser=parser)

    # then parse the args
    FLAGS = parser.parse_args()
    logger = set_up_logger(FLAGS.info_path, FLAGS.modelname)
    controller = cont.Controller(FLAGS)

    if FLAGS.mask == 'True':
        logger.debug('mask')
        controller.evaluate_masked_set(filepath=FLAGS.validdata)
    elif FLAGS.infer == 'True':
        logger.debug('infer')
        controller.init_for_infer()
        controller.interactive_inference()
    elif FLAGS.sequence:
        logger.debug('infering single sequence')
        controller.init_for_infer()
        preds = controller.infer(FLAGS.sequence)
        with open(os.path.join(FLAGS.info_path, 'results.txt'), 'w') as ofile:
            ofile.write(preds)
        logger.debug(preds)
    elif FLAGS.test == 'True':
        logger.debug('test')
        controller.test()
    else:
        logger.debug('train')
        controller.train()

    logger.info('Done.')


if __name__ == '__main__':
    main()
