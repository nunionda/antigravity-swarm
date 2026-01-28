"""
BioSwarm: PDB Parser
Extracts atomic coordinates from PDB files.
"""
import numpy as np

class PDBParser:
    @staticmethod
    def parse_pdb(pdb_path: str):
        """
        Parses PDB and returns atoms and secondary structure mapping.
        """
        atoms = []
        helices = [] # List of (start_res_num, end_res_num)
        sheets = []  # List of (start_res_num, end_res_num)
        
        with open(pdb_path, 'r') as f:
            for line in f:
                try:
                    if line.startswith("HELIX"):
                        start = int(line[21:25].strip())
                        end = int(line[33:37].strip())
                        helices.append((start, end))
                    elif line.startswith("SHEET"):
                        start = int(line[22:26].strip())
                        end = int(line[33:37].strip())
                        sheets.append((start, end))
                    elif line.startswith("ATOM"):
                        name = line[12:16].strip()
                        res_num_str = line[22:26].strip()
                        if not res_num_str: continue
                        res_num = int(res_num_str)
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        
                        # Secondary Structure mapping
                        ss = "C" # Coil
                        for h_start, h_end in helices:
                            if h_start <= res_num <= h_end:
                                ss = "H" # Helix
                                break
                        for s_start, s_end in sheets:
                            if s_start <= res_num <= s_end:
                                ss = "S" # Sheet
                                break
                                
                        if name == "CA":
                            atoms.append({
                                "name": name,
                                "pos": [x, y, z],
                                "ss": ss
                            })
                except (ValueError, IndexError):
                    continue
        if not atoms:
            print(f"⚠️ [PDB] No CA atoms found in {pdb_path}. Check format.")
            
        return atoms
