import logging


def logger_config(args):
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('my_script.log') if args.log_to_file else logging.StreamHandler()
        ]
    )
