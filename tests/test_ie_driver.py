import os
import sys

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.driver import IEDriver
from webdriver_manager.microsoft import IEDriverManager


@pytest.mark.parametrize("version", ["2.53.1",
                                     "3.0",
                                     "latest",
                                     None,
                                     pytest.mark.xfail("0.2")])
@pytest.mark.parametrize("use_cache", [True,
                                       False])
@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
def test_ie_manager_with_selenium(version, use_cache):
    delete_cache()
    if use_cache:
        IEDriverManager(version).install()
    driver_path = IEDriverManager(version).install()
    dr = webdriver.Ie(driver_path)
    dr.quit()


@pytest.mark.parametrize("version", ["2.53.1",
                                     "3.0",
                                     "latest",
                                     None,
                                     pytest.mark.xfail("0.2")])
@pytest.mark.parametrize("use_cache", [True,
                                       False])
def test_ie_driver_binary(version, use_cache):
    delete_cache()
    ie_driver = IEDriver(version, "win32")
    if use_cache:
        cache.download_driver(ie_driver)
    ie_driver_bin = cache.download_driver(ie_driver)
    assert ie_driver_bin.name == u'IEDriverServer'
    assert os.path.exists(ie_driver_bin.path)
