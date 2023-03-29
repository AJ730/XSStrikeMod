import copy
import re

from selenium.webdriver import chrome

import core.config
from core.colors import green, end
from core.config import xsschecker
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.requester import requester
from core.log import setup_logger
from xss.browser_simulator.chrome_simulator.chrome_sim import ChromeSimulator
from xss.reader.LogStorer import LogStorer

logger = setup_logger(__name__)

logStorer = LogStorer()

def logVector(chrome, payload, loggerVector, url, paramName, vector):
    popup = chrome.validate_get_attack(payload)
    if popup:
        logger.red_line()
        logger.good('Payload: %s' % loggerVector)

    print(popup)
    logStorer.addVector(popup, url, paramName, vector, payload)


def crawl(scheme, host, main_url, form, blindXSS, blindPayload, headers, delay, timeout, encoding):
    chrome = ChromeSimulator()

    if form:
        for each in form.values():
            url = each['action']
            if url:
                if url.startswith(main_url):
                    pass
                elif url.startswith('//') and url[2:].startswith(host):
                    url = scheme + '://' + url[2:]
                elif url.startswith('/'):
                    url = scheme + '://' + host + url
                elif re.match(r'\w', url[0]):
                    url = scheme + '://' + host + '/' + url
                if url not in core.config.globalVariables['checkedForms']:
                    core.config.globalVariables['checkedForms'][url] = []
                method = each['method']
                GET = True if method == 'get' else False
                inputs = each['inputs']
                paramData = {}
                for one in inputs:
                    paramData[one['name']] = one['value']
                    for paramName in paramData.keys():
                        if paramName not in core.config.globalVariables['checkedForms'][url]:
                            core.config.globalVariables['checkedForms'][url].append(paramName)
                            paramsCopy = copy.deepcopy(paramData)
                            paramsCopy[paramName] = xsschecker
                            response = requester(
                                url, paramsCopy, headers, GET, delay, timeout)
                            occurences = htmlParser(response, encoding)
                            positions = occurences.keys()
                            occurences = filterChecker(
                                url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
                            vectors = generator(occurences, response.text)


                            if vectors:
                                for confidence, vects in vectors.items():
                                    try:
                                        vector = list(vects)[0]
                                        payload = f"{main_url}?{paramName}={vector}"
                                        logVector(chrome, payload, vector, url, paramName, vector)
                                        break
                                    except IndexError:
                                        pass


                            # if blindXSS and blindPayload:
                            #     paramsCopy[paramName] = blindPayload
                            #     requester(url, paramsCopy, headers,
                            #               GET, delay, timeout)

