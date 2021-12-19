import re
from .iolayer.pdbsupport import PDBmixin

file = '/home/frgoetz/work/docker/pdbs/5RGQ.pdb'

class Docker(PDBmixin):
    def __init__(self):
        pass

pdb_info = Docker.ReadPdb(filepath=file)

keys = pdb_info.keys()


        
        