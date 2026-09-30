import sys

def print_usage():
    sys.stderr.write("USAGE: {0:s} <in_file> <out_file>\n".format(sys.argv[0]))
    sys.stderr.write("       <in_file> .... Input file name.\n")
    sys.stderr.write("       <out_file> ... Output file name (optional).\n")
    return

if len(sys.argv) < 2 or sys.argv[1] in ["-?", "-h", "--help"]:
    print_usage()
    sys.exit(1)

infile_path = sys.argv[1]
if len(sys.argv) == 3:
    outfile_path = sys.argv[2]
else:
    outfile_path = None

def read_structure_file(file_path):
    """
    Read the structure information from a file and return a list of dictionaries.
    Each dictionary represents a structure with keys: 'lattice', 'atoms', 'energy', and 'charge'.
    """
    structures = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        structure = {}
        for line in lines:
            if line.strip():  # Skip empty lines
                if line.startswith("begin"):
                    structure = {}
                elif line.startswith("end"):
                    structures.append(structure)
                else:
                    key, *values = line.split()
                    if key == "comment":
                        structure["comment"] = values
                    elif key == "atom":
                        if "atoms" not in structure:
                            structure["atoms"] = []
                        atom_info = {
                            "element": str(values[3]),
                            "x": float(values[0]),
                            "y": float(values[1]),
                            "z": float(values[2]),
                            "fx": float(values[6]),
                            "fy": float(values[7]),
                            "fz": float(values[8]),
                        }
                        structure["atoms"].append(atom_info)
                        structure["atom_number"] = str(len(structure["atoms"]))
                    elif key == "lattice":
                        # Assume lattice information
                        if "lattices" not in structure:
                            structure["lattices"] = []
                        structure["lattices"].append(str(values[0]))
                        structure["lattices"].append(str(values[1]))
                        structure["lattices"].append(str(values[2]))
                    elif key == "energy":
                        structure["energy"] = float(values[0])
    return structures

def write_structure_file(file_path, structures):
    """
    Write the list of structures to a file in the specified format.
    """

    with open(file_path, 'w') as f:
        for i in range (len(structures)):    
            f.write((structures[i]["atom_number"]) + "\n")
            lattice_str = " ".join(structures[i]["lattices"])
            f.write(f'Lattice="{lattice_str}" Properties=species:S:1:pos:R:3:forces_dft:R:3 energy_dft={structures[i]["energy"]}\n')
            for atom in structures[i].get("atoms", []):
                f.write(f"{atom['element']:<2} {atom['x']:>12.8f} {atom['y']:>12.8f} {atom['z']:>12.8f} {atom['fx']:>12.8f} {atom['fy']:>12.8f} {atom['fz']:>12.8f}\n")

addstructures = read_structure_file(infile_path)
write_structure_file(outfile_path, addstructures)
