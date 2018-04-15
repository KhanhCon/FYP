import requests

def downloadComposerJson(github_fullname, SHA_number):
    r = requests.get('https://raw.githubusercontent.com/' + github_fullname + '/' + SHA_number + '/composer.json')
    # print('https://raw.githubusercontent.com/' + github_fullname + '/' + SHA_number + '/composer.json')
    if r.status_code != 404:
        try:
            return r.json()
        except ValueError:
            return None
    else:
        return None

def composerJson_validate(github_fullname, SHA_number):
    import urllib
    testfile = urllib.URLopener()
    file = SHA_number + "composer.json"
    try:
        testfile.retrieve('https://raw.githubusercontent.com/' + github_fullname + '/' + SHA_number + '/composer.json', file)
    except IOError: #Sometimes they delete composer.json back in the days
        print("IO Error")
        return False
    import os
    code = os.system("composer validate " + file + " --no-check-publish ") #Output to NUL to surpress output
                                                                    # Strict nocheck
    os.remove(file)
    if code != 0:
        return False
    return True


def getDependenciesNames(json):
    if json is not None and json:

        if ("name") in json:
            packagist_name = json["name"]

        # print(name)
        if "require-dev" in json and "require" in json:
            l1 = json["require"]
            require = json["require-dev"]
            require.update(l1)

        elif "require" in json:
            require = json["require"]
        elif "require-dev" in json:
            require = json["require-dev"]
        else:
            print("@@")
            require = None
    else:
        print("@@")
        require = None
    return packagist_name, require


def getPackageFromPackagist(name):
    r = requests.get('https://packagist.org/packages/'+ name +'.json')
    if r.status_code == 200:
        package = r.json()["package"]
        return {"name": package["name"],
                "description": package["description"],
                "maintainers": package["maintainers"],
                "github_fullname": package["repository"][19:],
                "type": package["type"]
                }
    return None

## With a name found in composer.json. Find its information on packagist
def getPackagistName(name):
    payload = {'q': name, 'per_page': 20}
    r = requests.get('https://packagist.org/search.json', params=payload)
    results = r.json()["results"]
    for result in results:
        print(result["repository"])
        if result["name"] == name and result["repository"] == "":
            return result
    return None

if __name__ == "__main__":
    # print(getPackagistName("laravel/laravel"))
    r = requests.get('https://packagist.org/packages/laravel/laravel.json')
    print getPackageFromPackagist('phpunit/phpunit')
    print(r.status_code)
    s = 'https://github.com/laravel/laravel'

    print s[19:]