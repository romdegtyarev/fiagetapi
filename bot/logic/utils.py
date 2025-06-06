import os
import re


def safe_name(s: str) -> str:
    """
    #TODO.

    :param s: #TODO.
    :return: #TODO.
    """
    return re.sub(r'\W+', '_', s)


def make_data_filename(prefix: str, session, ext: str = "png") -> str:
    """
    #TODO.

    :param prefix: #TODO.
    :param session: A FastF1 session object.
    :param ext: #TODO.
    :return: #TODO.
    """
    event = session.event
    year = event['EventDate'].year
    gp = safe_name(event['EventName'])
    type_name = safe_name(session.name)
    filename = f"data/{prefix}_{year}_{gp}_{type_name}.{ext}"
    os.makedirs("data", exist_ok=True)
    return filename
