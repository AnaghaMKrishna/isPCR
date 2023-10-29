import subprocess

def step_three(hit_pairs: list[tuple[list[str]]], assembly_file: str) -> str:
    bed_file = create_bed_file(hit_pairs)
    amplicon = call_seqtk(assembly_file, bed_file)
    return amplicon

def create_bed_file(hit_pairs: list[tuple[list[str]]]) -> str:
    bed_list = []
    for amplicon_pair in hit_pairs:
        primer1, primer2 = amplicon_pair
        bed_list.append(f"{primer1[1]}\t{primer1[9]}\t{int(primer2[9])-1}")
    
    bed_file = ('\n').join(bed_list)

    # print(repr(bed_file))
    return bed_file

def call_seqtk(assembly_file: str, bed_file: str) -> str:
    # amplicon_seq = subprocess.run(f'echo "{bed_file}" > data/Vibrio_cholerae_N16961.bed ; seqtk subseq {assembly_file} data/Vibrio_cholerae_N16961.bed', \
    #             shell=True, \
    #             capture_output=True, \
    #             text=True, \
    #             executable="/bin/bash"
    #             )
    amplicon_seq = subprocess.run(f'seqtk subseq {assembly_file} <(echo "{bed_file}" ; data/Vibrio_cholerae_N16961.bed | xargs)', \
                   shell=True, \
                   capture_output=True, \
                   text=True, \
                   executable="/bin/bash"
                   )
    # print(amplicon_seq)
    return amplicon_seq.stdout