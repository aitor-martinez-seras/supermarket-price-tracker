from pathlib import Path


# TODO: Preguntar a Aritz cual es la mejor manera de hacer esta operacion de importar los user agents
URLS_EXCEL = r"LIBRO-BASE-PRODUCTOS_ok.xlsx"
RESOURCES_PATH = Path('resources')
"""
with open(RESOURCES_PATH / 'user-agents.txt', 'r') as f:
    USER_AGENTS = []
    for line in f:
        strip_lines = line.strip()
        USER_AGENTS.append(strip_lines)
"""
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


