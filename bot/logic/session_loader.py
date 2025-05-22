import fastf1


def load_session(year, gp, sess_type):
    session = fastf1.get_session(year, gp, sess_type)
    session.load()
    return session
