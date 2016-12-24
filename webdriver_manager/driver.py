import requests

from webdriver_manager.utils import OSUtils


class Driver(object):
    def __init__(self, driver_url, name, version):
        self._url = driver_url
        self.name = name
        self._version = version

    def get_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self._url,
                          ver=self.get_version(),
                          name=self.name,
                          os=OSUtils.os_name() + str(OSUtils.os_architecture()))

    def get_version(self):
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version

    def get_latest_release_version(self):
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, driver_url, name, version):
        super(ChromeDriver, self).__init__(driver_url, name, version)

    def get_latest_release_version(self):
        file = requests.get(self._url + "/LATEST_RELEASE")
        return file.text.rstrip()


class FireFoxDriver(Driver):
    def __init__(self, driver_url, name, version):
        super(FireFoxDriver, self).__init__(driver_url, name, version)

    def get_latest_release_version(self):
        resp = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest?access_token=d402775fc19618cebd806a0b5856c84b83697b92")
        return resp.json()["tag_name"]

    def get_url(self):
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz

        resp = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}?access_token=d402775fc19618cebd806a0b5856c84b83697b92".format(self.get_version()))

        os = OSUtils.os_name() + str(OSUtils.os_architecture())
        assets = resp.json()["assets"]
        ver = self.get_version()
        name = self.name + "-" + ver + "-" + os
        output_dict = [asset for asset in assets if asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']
