from naptax.analyze.GLCodeValidator import GLCodeValidator
from data.GLTaxSettingsByState import GLTaxSettingsByState


def run():
    test_validator = GLCodeValidator(GLTaxSettingsByState)
    print(test_validator.gl_dict)
    print(test_validator.unused_gl)
    #print(test_validator.check_unused_gl("4012"))


if __name__ == "__main__":
    run()
