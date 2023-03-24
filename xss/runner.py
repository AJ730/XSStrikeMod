from time import sleep

from xss.browser_simulator.chrome_simulator.chrome_sim import ChromeSimulator

if __name__ == '__main__':
    c = ChromeSimulator()
    c.get_browser()
    c.accept_license()

    c.search_address("http://www.facebook.com")
    print(c.get_current_address_url())
    c.halt(200)