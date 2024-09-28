import abjad
import evans

h_rotation = (
    evans.Sequence([[12, 12, 10], [12, 13, 16, 18], [22, 20, 18, 15, 14, 9]])
    .helianthate(-1, 1)
    .flatten(depth=-1)
)
sigs = evans.CyclicList(
    evans.Sequence(
        [abjad.TimeSignature((_, 16)) for _ in h_rotation]
    ).reduce_time_signatures_in_list(),
    forget=False,
)

##
## 01 ##
##

signatures_01 = sigs(r=166)

signatures_01.append(abjad.TimeSignature((1, 4)))  # for ending skip

fermata_measures_01 = [1, 8, 14, 18, 42, 47, 80, 83, 85, 89, 99, 103, 165]

reduced_signatures_01 = evans.reduce_fermata_measures(
    signatures_01, fermata_measures_01
)

##
## total ##
##

all_signatures = evans.join_time_signature_lists(
    [
        reduced_signatures_01,
    ]
)
