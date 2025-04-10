import os

REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), "requirements.txt")

def read_requirements():
    """ 📌 Lit les dépendances depuis requirements.txt """
    if not os.path.exists(REQUIREMENTS_FILE):
        print("❌ Fichier requirements.txt introuvable !")
        exit(1)

    with open(REQUIREMENTS_FILE, "r") as f:
        modules = [line.strip().split("==")[0] for line in f.readlines() if line.strip()]
    return modules

REQUIRED_MODULES = read_requirements()

missing_modules = []

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if len(missing_modules) > 0:
    exit(1)
exit(0)
