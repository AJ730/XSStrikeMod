from xss.browser_simulator.chrome_simulator.chrome_sim import ChromeSimulator

if __name__ == '__main__':
    c = ChromeSimulator()
    c.get_browser()
    c.halt(10)