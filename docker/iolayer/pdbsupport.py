import re

class PDBmixin:
    @classmethod
    def ReadPdb(cls, filepath: str) -> dict:
        """[summary]

        Args:
            filepath (str): Path to a PDB file.

        Returns:
            dict: A dictonary containning the extracted data with the following hierarchy:
            [chain_id]
                [res_id]
                    [atom_id]
                        ['element_id']
                        ['amino_acid']
                        ['temperature_factor']
                        ['x']
                        ['y']
                        ['z']
                        ['occupancy']
                        ['element']
        """

        atom_regex1 = 'ATOM\s+(?P<atom_id>\d+)\s+(?P<element_id>\S+)\s+(?P<amino_acid>\S+)\s+(?P<chain_id>\S)\s+(?P<residue_id>\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+(?P<occupancy>\S+)\s+(?P<temperature_factor>\S+)\s+(?P<element>\S+)\s+'
        atom_regex2 = 'ATOM\s+(?P<atom_id>\d+)\s+(?P<element_id>\S\S\S)(?P<amino_acid>\S+)\s+(?P<chain_id>\S)\s+(?P<residue_id>\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+(?P<occupancy>\S+)\s+(?P<temperature_factor>\S+)\s+(?P<element>\S+)\s+'

        atom_regex1 = re.compile(atom_regex1)
        atom_regex2 = re.compile(atom_regex2)

        regexes = [atom_regex1, atom_regex2]

        pdb_info = {}

        prop_list = ['element_id', 'amino_acid', 'temperature_factor', 'x', 'y', 'z', 'occupancy', 'element']

        with open(filepath, 'r') as f:
            for regex in regexes:
                matches = re.finditer(regex, f.read())
                for match in matches:

                    chain_id = match.group('chain_id')
                    if not chain_id in pdb_info:
                        pdb_info[chain_id] = {}

                    res_id = match.group('residue_id')
                    if not res_id in pdb_info[chain_id]:
                        pdb_info[chain_id][res_id] = {}

                    atom_id = match.group('atom_id')
                    if not atom_id in pdb_info[chain_id][res_id]:
                        pdb_info[chain_id][res_id][atom_id] = {}

                    for prop in prop_list:
                        pdb_info[chain_id][res_id][atom_id][prop] = match.group(prop)

            return cls(pdb_info)