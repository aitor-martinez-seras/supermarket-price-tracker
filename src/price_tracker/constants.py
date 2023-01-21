from pathlib import Path
import os

# TODO: Preguntar a Aritz cual es la mejor manera de hacer esta operacion de importar los user agents

# Folder name (by default)
FOLDER_NAME = "supermarket-price-tracker"

# Root path
cwd = os.getcwd()
ROOT_PATH = Path(cwd[:cwd.find(FOLDER_NAME)+len(FOLDER_NAME)])

# Price_tracker package
PACKAGE_PATH = ROOT_PATH / 'src/price_tracker'

# Configs
CONFIGS_PATH = PACKAGE_PATH / 'configs'
SMTP_CFG_PATH = CONFIGS_PATH / 'smtp.toml'

# Logs
LOGS_PATH = ROOT_PATH / 'logs/'

# Resources
RESOURCES_PATH = PACKAGE_PATH / 'resources/'
URLS_EXCEL_PATH = RESOURCES_PATH / r'Lista_de_productos.xlsx'

# Outputs
OUTPUTS_PATH = PACKAGE_PATH / 'outputs'


UNITS = {
    "litro": ["litro", "litros"],
    "kilo": ["kilo", "kilos", "kg"],
    "mililitro": ["mililitro", "ml"],
    "unidad": ["unidad", "ud", "uds"],
    "dosis": ["dosis"],
    "docena": ["docena"],
    "metro": ["metro"],
    "rollo": ["rollo"],
    "manojo": ["manojo"],
    "botella": ["botella"]
}

MONTHS = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

"""
with open(RESOURCES_PATH / 'user-agents.txt', 'r') as f:
    USER_AGENTS = []
    for line in f:
        strip_lines = line.strip()
        USER_AGENTS.append(strip_lines)
"""
