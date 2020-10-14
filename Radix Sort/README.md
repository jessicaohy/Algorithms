# Radix Sort

Sorting and Collating:
- Time complexity = O(TM), where
    T is the total number of words over all songs in input file
    M is the length of the longest word
Lookup:
- Time complexity = O(q x Mlog(U) + P), where
    q is th enumber of words in query_file
    M is the length of the longest word in any song
    U is the number of lines in collated_file
    P is the total number of IDs in the output
