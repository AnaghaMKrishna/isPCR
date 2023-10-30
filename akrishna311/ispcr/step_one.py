import subprocess

PCT_MATCH = 80.00

def step_one(primer_file: str, assembly_file: str) -> list[list[str]]:
    """
    to identify locations where primers would anneal to the target sequence

    Args:
        primer_file: file path of the primer file
        assembly_file: file path the assembly file

    Returns:
        list containing the filtered blast outputs
    """
    blast_output = call_blast(primer_file, assembly_file)
    filtered_blast_output = filter_blast(blast_output)
    
    return filtered_blast_output

def call_blast(primer_file: str, assembly_file: str) -> str:
    """
    to blast primer sequence against assembly file to find sequence matches

    Args:
        primer_file: file path of the primer file
        assembly_file: file path the assembly file

    Returns:
        output of blast
    """
    blast_output = subprocess.run(["blastn", "-task", "blastn-short", "-query", primer_file, "-subject", assembly_file, "-outfmt", '6 std qlen'], \
                   capture_output=True, \
                   text=True
                   )
    return blast_output.stdout

def filter_blast(blast_output:str) -> list[list[str]]:
    """
    filter blast hits to extracts hits which match atleast a predefined threshold PCT_MATCH and store it as a list of strings

    Args:
        blast_output: output of blast

    Returns:
        list of sorted list of blast hits with match percent above PCT_MATCH
    """
    filtered_blast_output = subprocess.run("awk '{if ($3 >= PCT_MATCH && $4 == $13 ) print $0;}' | sort -k 9,10n", \
                                           capture_output=True, \
                                           text=True, \
                                           shell=True, \
                                           input=blast_output
                                           )
    blast_output_list = filtered_blast_output.stdout.split('\n')
    blast_output_fields = [i.split('\t') for i in blast_output_list[:-1]] #exclude last entry to get rid of unwanted newline
    
    return blast_output_fields