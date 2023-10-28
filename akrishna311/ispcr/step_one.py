import subprocess

PCT_MATCH = 80.00

def step_one(primer_file: str, assembly_file: str) -> list[list[str]]:
    blast_output = call_blast(primer_file, assembly_file)
    filtered_blast_output = filter_blast(blast_output)
    return filtered_blast_output

def call_blast(primer_file: str, assembly_file: str) -> str:
    blast_output = subprocess.run(["blastn", "-task", "blastn-short", "-query", primer_file, "-subject", assembly_file, "-outfmt", '6 std qlen'], \
                   capture_output=True, \
                   text=True
                   )
    return blast_output.stdout

def filter_blast(blast_output:str) -> str:
    filtered_blast_output = subprocess.run("awk '{if ($3 >= PCT_MATCH && $4 == $13 ) print $0;}'", \
                                           capture_output=True, \
                                           text=True, \
                                           shell=True, \
                                           input=blast_output
                                           )
    blast_output_list = filtered_blast_output.stdout.split('\n')
    blast_output_fields = [i.split('\t') for i in blast_output_list[:-1]]
    return blast_output_fields