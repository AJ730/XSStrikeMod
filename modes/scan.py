import copy
import sys
from urllib.parse import urlparse, quote, unquote
from pywebcopy import save_webpage
from core.checker import checker
from core.colors import end, green, que
import core.config
from core.config import xsschecker, minEfficiency
from core.dom import dom
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.requester import requester
from core.utils import getUrl, getParams, getVar, writer
from core.wafDetector import wafDetector
from core.log import setup_logger
from xss.browser_simulator.chrome_simulator.chrome_sim import ChromeSimulator

import os, sys, re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from xss.reader.LogStorer import LogStorer

logger = setup_logger(__name__)
logStorer = LogStorer()


def write_vectors(vectors, filename):
    with open(filename, 'w') as f:
        for vs in vectors.values():
            for v in vs:
                f.write("{}\n".format(v))
    logger.info('Written payloads to file')


def scan(target, paramData, encoding, headers, delay, timeout, skipDOM, skip, payloads_file, find=""):
    GET, POST = (False, True) if paramData else (True, False)
    # If the user hasn't supplied the root url with http(s), we will handle it

    chrome = ChromeSimulator()

    if not target.startswith('http'):
        try:
            response = requester('https://' + target, {},
                                 headers, GET, delay, timeout)
            target = 'https://' + target
        except:
            target = 'http://' + target
    logger.debug('Scan target: {}'.format(target))
    response = requester(target, {}, headers, GET, delay, timeout).text
    host = urlparse(target).netloc  # Extracts host out of the url
    logger.debug('Host to scan: {}'.format(host))
    url = getUrl(target, GET)
    logger.debug('URL to scan: {}'.format(url))
    params = getParams(target, paramData, GET)
    logger.debug_json('Scan parameters:', params)

    if not params:
        logger.error('No parameters to test.')
        quit()
    WAF = wafDetector(
        url, {list(params.keys())[0]: xsschecker}, headers, GET, delay, timeout)
    if WAF:
        logger.error('WAF detected: %s%s%s' % (green, WAF, end))
    else:
        logger.good('WAF Status: %sOffline%s' % (green, end))
    if not skipDOM:
        logger.run('Checking for DOM vulnerabilities')
        highlighted = dom(response, params)
        if highlighted:
            logger.good('Potentially vulnerable objects found')
            logger.red_line(level='good')
            for line in highlighted:
                logger.no_format(line, level='good')
            logger.red_line(level='good')

    for paramName in params.keys():
        paramsCopy = copy.deepcopy(params)
        logger.info('Testing parameter: %s' % paramName)
        if encoding:
            paramsCopy[paramName] = encoding(xsschecker)
        else:
            paramsCopy[paramName] = xsschecker
        response = requester(url, paramsCopy, headers, GET, delay, timeout)
        occurences = htmlParser(response, encoding)
        positions = occurences.keys()
        logger.debug('Scan occurences: {}'.format(occurences))
        if not occurences:
            logger.error('No reflection found')
            continue
        else:
            logger.info('Reflections found: %i' % len(occurences))

        logger.run('Analysing reflections')
        efficiencies = filterChecker(
            url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
        logger.debug('Scan efficiencies: {}'.format(efficiencies))
        logger.run('Generating payloads')
        vectors = generator(occurences, response.text)
        total = 0
        for v in vectors.values():
            total += len(v)
        if total == 0:
            logger.error('No vectors were crafted.')
            continue
        logger.info('Payloads generated: %i' % total)
        logger.debug(f'payload_file: {payloads_file}')
        if payloads_file:
            write_vectors(vectors, payloads_file)
        progress = 0

        for confidence, vects in vectors.items():
            for vect in vects:
                if core.config.globalVariables['path']:
                    vect = vect.replace('/', '%2F')
                loggerVector = vect
                progress += 1
                logger.run('Progress: %i/%i\r' % (progress, total))
                if not GET:
                    vect = unquote(vect)

                efficiencies = checker(
                    url, paramsCopy, headers, GET, delay, vect, positions, timeout, encoding)
                if not efficiencies:
                    for i in range(len(occurences)):
                        efficiencies.append(0)
                bestEfficiency = max(efficiencies)

                queryParam = next(iter(paramsCopy))

                payload = f"{url}?{queryParam}={vect}"

                if bestEfficiency == 100 or (vect[0] == '\\' and bestEfficiency >= 95):

                    logVector(chrome, payload, loggerVector, bestEfficiency, confidence, url, queryParam, vect)
                    if skip:
                        return target, loggerVector
                elif bestEfficiency > minEfficiency:
                    logVector(chrome, payload, loggerVector, bestEfficiency, confidence, url, queryParam, vect)
        logger.no_format('')

    chrome.kill_chrome()


def logVector(chrome, payload, loggerVector, bestEfficiency, confidence, url, paramName, vector):
    popup = chrome.validate_get_attack(payload)
    if popup:
        logger.red_line()
        logger.good('Payload: %s' % loggerVector)
        logger.info('Efficiency: %i' % bestEfficiency)
        logger.info('Confidence: %i' % confidence)
    logStorer.addVector(popup, url, paramName, vector, payload)
