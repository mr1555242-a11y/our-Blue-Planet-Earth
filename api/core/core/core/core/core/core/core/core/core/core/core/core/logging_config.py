import logging


def configure_logging():

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(message)s"
        )
    )

    return logging.getLogger(
        "our_blue_planet"
    )


logger = configure_logging()
