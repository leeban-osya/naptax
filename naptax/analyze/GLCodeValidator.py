__author__ = 'nabeelh-dev'

class GLCodeValidator(object):
    """
    Will load GL Code settings from data/GLTaxSettingsByState.py
    Will build a set of GL codes that are set to False for all States.
    This will be to quickly discard an invoice row if we won't be taxed on it in any state.

    GLCodeValidator.query_gl_state(gl_code, state_abrev) will be the core functionality.
    Will return True or False depending on if GL Code is taxed in that State.
    """
    def __init__(self, gl_dict):
        self.gl_dict = gl_dict
        self.unused_gl = self.generate_unused_gl()

    def generate_unused_gl(self):
        """
        Identifies which gl codes are not taxable for all state gl settings.
        Returns a set and sets it to self.unused_gl.
        Run when GlCodeValidator is created.
        :input: self.gl_dict : dict
        :return: unused_gl : set
        """
        false_gl_count = {}
        total_states = 0
        for k, v in self.gl_dict.items():
            total_states += 1
            for gl_code, val in v.items():
                if not val:
                    false_gl_count[gl_code] = false_gl_count.get(gl_code, 0) + 1
        return {x for x, v in false_gl_count.items() if v == total_states}

    def check_unused_gl(self, gl_code):
        """
        Returns True if gl_code is in self.unused_gl list or False
        If gl_code is in that list then we should not process that invoice line.
        If False then check to see
        :param gl_code: str
        :return: gl_unused: Bool
        """
        return gl_code in self.unused_gl

    def check_gl_state(self, gl_code, state_abrv):
        if self.check_unused_gl(gl_code):
            return False
        return self.gl_dict[state_abrv][gl_code]

# TODO: Add way to convert SAR to appropriate State.