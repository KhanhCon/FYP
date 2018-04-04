import os

# print(os.system("composer validate --strict"))


def composerJson_validate(name, SHA_number):
    import urllib
    testfile = urllib.URLopener()
    file = SHA_number + "composer.json"
    testfile.retrieve('https://raw.githubusercontent.com/' + name + '/' + SHA_number + '/composer.json', file)
    import os
    code = os.system("composer validate " + file + " --strict > NUL 2>&1")
    os.remove(file)
    if code != 0:
        return False
    return True

print os.system("composer validate composer.json --strict --no-check-publish")
# print composerJson_validate("moneyphp/money", "866e0f1b7857561efe94a3320c2f6cbe8f3a2965")
