import requests, MyGithub

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


def getDependenciesNames(github_name, SHA_number):
    status = MyGithub.continous_integration_status(name=github_name, SHA_number=SHA_number)
    if status == "fail":
        print("continous integration fail")
        return None
    elif status == "none":
        if composerJson_validate(github_name, SHA_number) == False:
            print("invalid composerJson")
            return None

    json = downloadComposerJson(github_name, SHA_number)

    if json is not None and json:
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
    try:
        del require["php"]
    except:
        return require
    return  require


def getPackageFromPackagist(name):
    r = requests.get('https://packagist.org/packages/'+ name +'.json')
    # print r.status_code
    # print name
    if r.status_code == 200:
        try:
            package = r.json()["package"]
        except:
            return None
        return {"name": package["name"],
                "description": package["description"],
                "maintainers": package["maintainers"],
                "github_fullname": package["repository"][19:],
                # "type": package["type"]
                }
    return None #None if can't find package

def getDependenciesPackages(github_name, SHA_number):
    dependencyNames = getDependenciesNames(github_name, SHA_number)
    if dependencyNames == None:
        return None
    dependencyPackages = []
    for dependency in dependencyNames:
        dependencyPackage = getPackageFromPackagist(dependency)
        if dependencyPackage == None:
            print dependency, "no packagist"
            continue
        dependencyPackages.append(dependencyPackage)
    return dependencyPackages

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

    import dateutil.parser, datetime
    yourdate = dateutil.parser.parse('2012-03-06T22:42:09Z')
    yourdate = yourdate + datetime.timedelta(seconds=1)


    print yourdate.isoformat()

    # # print(getPackagistName("laravel/laravel"))
    # r = requests.get('https://packagist.org/packages/laravel/laravel.json')
    # print getPackageFromPackagist('InvoicePlane/InvoicePlane')
    # # print(r.status_code)
    # s = 'https://github.com/laravel/laravel'
    #
    # s[19:]
    #
    #
    # l = [0,1,2,3,4]
    #
    # for index, num in enumerate(l[2:]):
    #     print index+2
    # import json
    # with open('data.json') as json_data:
    #     names = json.load(json_data)
    # print(names[511])