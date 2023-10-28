import subprocess

def step_one(primer_file: str, assembly_file: str) -> list[list[str]]:
    blast_output = subprocess.run(["blastn", "-task", "blastn-short", "-query", primer_file, "-subject", assembly_file, "-outfmt", '6 std qlen'], \
                   capture_output=True, \
                   text=True
                   )
    filtered_blast_output = subprocess.run("awk '{if ($3 >= 80.000 && $4 == $13 ) print $0;}'", \
                                           capture_output=True, \
                                           text=True, \
                                           shell=True, \
                                           input=blast_output.stdout
                                           #executable="/bin/bash"
                                           )
    print(filtered_blast_output)
