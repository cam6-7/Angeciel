import os
import shutil
dossier = os.path.dirname(os.path.abspath(__file__))

shutil.rmtree(dossier + "/dossier")
os.makedirs(dossier + "/dossier")