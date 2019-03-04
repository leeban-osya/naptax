__author__ = 'nabeelh-dev'

class GLCodeValidator(object):
    """
    Will load GL Code settings from data/GLTaxSettingsByState.py
    Will build a set of GL codes that are set to False for all States.
    This will be to quickly discard an invoice row if we won't be taxed on it in any state.

    GLCodeValidator.query_gl_state(gl_code, state_abrev) will be the core functionality.
    Will return True or False depending on if GL Code is taxed in that State.
    """
    def __init__(self):
        pass