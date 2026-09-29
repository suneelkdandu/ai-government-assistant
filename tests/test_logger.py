from src.logger import get_logger


def test_logger():

    logger = get_logger(
        "govassist.test"
    )

    logger.info(
        "Logger initialized successfully."
    )

    logger.warning(
        "This is a test warning."
    )

    logger.error(
        "This is a simulated test error."
    )

    assert logger.name == "govassist.test"

    print(
        "TEST COMPLETED SUCCESSFULLY"
    )


if __name__ == "__main__":
    test_logger()