def step_two(sorted_hits: list[str], max_amplicon_size: int) -> list[tuple[list[str]]]:
    paired_hits = []
    paired_hits = find_amplicon_pairs(sorted_hits, max_amplicon_size, paired_hits)
    return paired_hits

def find_amplicon_pairs(sorted_hits: list[str], max_amplicon_size: int, paired_hits: list) -> list[tuple[list[str]]]:
    # Loop through all the sorted hits to check if any pair of hits satisfy conditions to make an amplicon
    # 1. Both primers anneal pointing towards one another
    # 2. Primers are sufficiently close to each other, set by max_amplicon_size
    for primer1 in sorted_hits:
        for primer2 in sorted_hits:
            valid_amplicon_pair = ()
            
            # We can skip comparing the same hits as they cannot make an amplicon
            if primer1 == primer2:
                continue
            else:
                # Check if both hits have the same sequence ID and primer IDs are not the same
                if primer1[1] == primer2[1] and primer1[0] != primer2[0]:
                    # Compare the 3' end of both primers and if their difference is less than amplicon size, they are valid pairs
                    if int(primer1[9]) < int(primer2[9]) and int(primer2[9]) - int(primer1[9]) < max_amplicon_size : #primer1[9] < primer1[10] and
                        valid_amplicon_pair = (primer1, primer2)
                        paired_hits.append(valid_amplicon_pair)

    return paired_hits
