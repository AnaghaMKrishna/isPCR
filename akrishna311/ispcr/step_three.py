import subprocess

def step_three(hit_pairs: list[tuple[list[str]]], assembly_file: str) -> str:
    """
    extracting amplicon sequences

    Args:
        hit_pairs: list of tuples with blast hit pairs which satisfy the condition of orientation and size
        assembly_file: file path for assembly file

    Returns:
        string with extracted amplicon sequences
    """
    bed_content = create_bed_file(hit_pairs)
    amplicon = call_seqtk(assembly_file, bed_content)
    amplicon_formatted = pretty_print(amplicon)
    
    return amplicon_formatted[:-1] #skip the newline at the end

def create_bed_file(hit_pairs: list[tuple[list[str]]]) -> str:
    """
    create bed file using the filtered amplicon list

    Args:
        hit_pairs: list containing hit pairs

    Returns:
        BED content as string
    """
    bed_list = []
    #extract seqID, amplicon co-ordinate which is the 3' end position of the two primers
    for amplicon_pair in hit_pairs:
        primer1, primer2 = amplicon_pair
        bed_list.append(f"{primer1[1]}\t{primer1[9]}\t{int(primer2[9])-1}")
    
    #create a string containing BED contents
    bed_content = ('\n').join(bed_list)
    return bed_content

def call_seqtk(assembly_file: str, bed_content: str) -> str:
    """
    execute seqtk to extract sequence from assembly file using coordinates in bed file

    Args:
        assembly_file: path to assembly file
        bed_file: BED content

    Returns:
        string of amplicon sequences extracted from hit positions
    """
    amplicon_seq = subprocess.run(f'seqtk subseq {assembly_file} <(echo "{bed_content}" ; data/Vibrio_cholerae_N16961.bed | xargs)', \
                   shell=True, \
                   capture_output=True, \
                   text=True, \
                   executable="/bin/bash"
                   )
    return amplicon_seq.stdout

def pretty_print(string: str, position: int = 83) -> str:
    """
    Break the sequence into readable lengths by adding newline character

    Args:
        string : long string to be broken
        position : index at which new line character should be added. Defaults to 83.
    
    Returns:
        String with added new line characters
    """
    str_list = string.split('\n')
    #for every even element in the list containing sequence, break the sequence into 'position' number of bases
    for line in range(1, len(str_list), 2):
        formatted_str = '\n'.join(str_list[line][i:i+position] for i in range(0, len(str_list[line]), position))
        str_list[line] = formatted_str
    
    return '\n'.join(str_list)