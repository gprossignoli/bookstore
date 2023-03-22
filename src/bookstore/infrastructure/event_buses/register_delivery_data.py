from datetime import datetime

from bookstore.settings import publication_data_logger


def register_delivery_data(function):
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        err = args[1]
        msg = args[2]
        if err:
            publication_data_logger.info(
                f"Event:{msg.key().decode('utf-8')},failed_delivery_at:{timestamp}"
            )
        else:
            publication_data_logger.info(
                f"Event:{msg.key().decode('utf-8')},delivered_at:{timestamp}"
            )
        function(*args, **kwargs)

    return wrapper
