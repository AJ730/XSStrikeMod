import copy
import re

import core.config
from core.colors import green, end
from core.config import xsschecker, minEfficiency
from core.checker import checker
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.requester import requester
from core.log import setup_logger
from xss.browser_simulator.chrome_simulator.chrome_sim import ChromeSimulator
from xss.reader.LogStorer import LogStorer

logger = setup_logger(__name__)
logStorer = LogStorer()


def crawl(scheme, host, main_url, form, blindXSS, blindPayload, headers, delay, timeout, encoding):
    chrome = ChromeSimulator()
    if form:

        for f in form.values():
            url = f['action']
            if url:
                # url fixing
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

                method = f['method']
                GET = method == 'get'  # True if method == 'get' else False
                inputs = f['inputs']
                paramData = {}

                for input in inputs:
                    paramData[input['name']] = input['value']
                    for paramName in paramData.keys():
                        if paramName not in core.config.globalVariables['checkedForms'][url]:
                            paramsCopy = copy.deepcopy(paramData)
                            core.config.globalVariables['checkedForms'][url].append(paramName)
                            if encoding:
                                paramsCopy[paramName] = encoding(xsschecker)
                            else:
                                paramsCopy[paramName] = xsschecker
                            response = requester(url, paramsCopy, headers, GET, delay, timeout)
                            occurences = htmlParser(response, encoding)
                            positions = occurences.keys()

                            occurences = filterChecker(url, paramsCopy, headers, GET, delay, occurences, timeout,
                                                       encoding)

                            vectors = generator(occurences, response.text)
                            if vectors:
                                for confidence, vects in vectors.items():
                                    for vect in vects:
                                        if core.config.globalVariables['path']:
                                            vect = vect.replace('/', '%2F')
                                        efficiencies = checker(url, paramsCopy, headers, GET, delay, vect, positions,
                                                               timeout, encoding)
                                        if not efficiencies:
                                            for i in range(len(occurences)):
                                                efficiencies.append(0)
                                        bestEfficiency = max(efficiencies)

                                        queryParam = next(iter(paramsCopy))

                                        payload = f"{url}?{queryParam}={vect}"

                                        if bestEfficiency == 100 or (vect[0] == '\\' and bestEfficiency >= 95):

                                            logVector(chrome, payload, vect, bestEfficiency, confidence, url, queryParam, vect)
                                        elif bestEfficiency > minEfficiency:
                                            logVector(chrome, payload, vect, bestEfficiency, confidence, url, queryParam, vect)
    else:
        print("issue with forms")
    chrome.kill_chrome()
    # try:
    #     payload = list(vects)[0]
    #     logger.vuln('Vulnerable webpage: %s%s%s' %
    #                 (green, url, end))
    #     logger.vuln('Vector for %s%s%s: %s' %
    #                 (green, paramName, end, payload))
    #     break
    # except IndexError:
    #     pass
    # if blindXSS and blindPayload:
    #     if type(blindPayload) is tuple:
    #         for x in blindPayload:
    #             paramsCopy[paramName] = x
    #             requester(url, paramsCopy, headers,
    #                       GET, delay, timeout)
    #     else:
    #         paramsCopy[paramName] = blindPayload
    #         requester(url, paramsCopy, headers,
    #                   GET, delay, timeout)


def logVector(chrome, payload, loggerVector, bestEfficiency, confidence, url, paramName, vector):
    popup = chrome.validate_get_attack(payload)
    if popup:
        logger.red_line()
        logger.good('Payload: %s' % loggerVector)
        logger.info('Efficiency: %i' % bestEfficiency)
        logger.info('Confidence: %i' % confidence)
    logStorer.addVector(popup, url, paramName, vector, payload)
