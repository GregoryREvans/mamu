import pathlib
from fractions import Fraction
from random import choice, seed

import abjad
import baca
import evans
from abjadext import rmakers

import mamu

cutaway_commands = [
    abjad.LilyPondLiteral(r"\stopStaff", site="before"),
    abjad.LilyPondLiteral(
        r"\override Staff.StaffSymbol.transparent = ##f", site="before"
    ),
    abjad.LilyPondLiteral(r"\override Staff.Rest.transparent = ##f", site="before"),
    abjad.LilyPondLiteral(r"\override Staff.Dots.transparent = ##f", site="before"),
    abjad.LilyPondLiteral(r"\startStaff", site="before"),
    evans.Attachment(
        abjad.LilyPondLiteral(r"\stopStaff", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    evans.Attachment(
        abjad.LilyPondLiteral(
            r"\override Staff.StaffSymbol.transparent = ##t", site="after"
        ),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    evans.Attachment(
        abjad.LilyPondLiteral(r"\override Staff.Rest.transparent = ##t", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    evans.Attachment(
        abjad.LilyPondLiteral(r"\override Staff.Dots.transparent = ##t", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    evans.Attachment(
        abjad.LilyPondLiteral(r"\startStaff", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
]


def trem_swell(selections):
    runs = abjad.select.runs(selections)
    for run in runs:
        if 1 < len(run):
            first_leaf = run[0]
            last_leaf = run[-1]
            abjad.attach(abjad.Dynamic("mf"), first_leaf)
            abjad.attach(abjad.StartHairpin("<"), first_leaf)
            abjad.attach(abjad.Dynamic("ff"), last_leaf)
            abjad.attach(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(r"\trem-one-markup"),
                        right_text=abjad.Markup(r"\trem-three-markup"),
                        style=r"solid-line-with-arrow",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                first_leaf,
            )
            abjad.attach(abjad.StopTextSpan(command=r"\stopTextSpanOne"), last_leaf)


kernel_motif = evans.PitchClassSegment([0, 11, 10, -5]).transpose(1)  # here
motif_sequence = (
    kernel_motif
    + kernel_motif.parallel()
    + kernel_motif.parallel().rotate(1).leittonwechsel()
    + kernel_motif.parallel().rotate(1).leittonwechsel().multiply(2).relative()
    + kernel_motif.parallel()
    .rotate(1)
    .leittonwechsel()
    .multiply(2)
    .relative()
    .retrograde()
    .wedge(1, 9, 1)
    + kernel_motif.parallel()
    .rotate(1)
    .leittonwechsel()
    .multiply(2)
    .relative()
    .retrograde()
    .wedge(1, 9, 1)
    .alpha(1)
)
motif_sequence = motif_sequence.to_sequence().remove_repeats().transpose(12)

lament_stops_1 = evans.Sequence([0, 11]).derive_added_sequences(motif_sequence)
lament_stops_2 = evans.Sequence([0, 10]).derive_added_sequences(motif_sequence)
lament_stops_3 = evans.Sequence([0, 9]).derive_added_sequences(motif_sequence)
lament_stops = [
    lament_stops_1[0],
    lament_stops_2[1],
    lament_stops_1[2],
    lament_stops_3[3],
    lament_stops_1[4],
    lament_stops_2[5],
    lament_stops_1[6],
    lament_stops_3[7],
    lament_stops_1[8],
    lament_stops_2[9],
    lament_stops_1[10],
    lament_stops_3[11],
]

violent_stops = []
cyc_accompaniment_interval = evans.CyclicList([11, 9, 10, 8, 13])
cyc_low_interval = evans.CyclicList([-7 - 1, -7 - 3, -7 - 2])
cyc_transpositions = evans.CyclicList(
    [0, 0, 0, 0, 0, 12, 12, 12, 0, 0, 12, 0, 12, 12, 0, 0, 0, 12, 12, 12, 12, 12]
)
for pitch in motif_sequence:
    pitch_ = pitch + cyc_transpositions(r=1)[0]
    violent_stops.append([pitch_, pitch_ + cyc_accompaniment_interval(r=1)[0]])
    violent_stops.append([-5, pitch_ + cyc_low_interval(r=1)[0]])

lament_figure = kernel_motif.invert(1).transpose(14).to_sequence()


maker = evans.SegmentMaker(
    instruments=mamu.instruments,
    names=[
        '"SCP"',
        '"BCP"',
        '" "',
        '" "',
        '"archi"',
    ],
    abbreviations=[
        '"SCP"',
        '"BCP"',
        '" "',
        '" "',
        '"archi"',
    ],
    name_staves=True,
    fermata_measures=mamu.fermata_measures_01,
    commands=[
        ## VIOLIN
        evans.attach(
            "string voice",
            abjad.LilyPondLiteral(r"\stopStaff", site="before"),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "string voice",
            abjad.LilyPondLiteral(
                r"\override Staff.StaffSymbol.transparent = ##t", site="before"
            ),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "string voice",
            abjad.LilyPondLiteral(
                r"\override Staff.Dots.transparent = ##t", site="before"
            ),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "string voice",
            abjad.LilyPondLiteral(r"\startStaff", site="before"),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "change voice",
            abjad.LilyPondLiteral(r"\stopStaff", site="before"),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "change voice",
            abjad.LilyPondLiteral(
                r"\override Staff.StaffSymbol.transparent = ##t", site="before"
            ),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "change voice",
            abjad.LilyPondLiteral(r"\startStaff", site="before"),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "change voice",
            abjad.LilyPondLiteral(
                r"\override Staff.Rest.transparent = ##t", site="before"
            ),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "change voice",
            abjad.LilyPondLiteral(
                r"\override Staff.Dots.transparent = ##t", site="before"
            ),
            selector=lambda _: abjad.select.leaf(_, 0),
        ),
        #### MUSIC
        evans.MusicCommand(
            ("violin voice", [0]),
            evans.note(),
            evans.PitchHandler(motif_sequence),
            evans.AfterGraceContainer(
                [abjad.Note("cs''16")],
                with_glissando=True,
                hide_accidentals=True,
                position=7,
            ),
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(6, 5, 3, 1, right_padding=0.5, match=True),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            abjad.Dynamic("sff"),
            abjad.StartHairpin(">o"),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            abjad.LilyPondLiteral(r"^\markup \upright {gridato}", site="after"),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.get.leaf(
                    abjad.select.leaf(_, -1),
                    1,
                ),
            ),
        ),
        evans.MusicCommand(
            ("string voice", (2, 8)),
            evans.talea([1, 1, 2, 3, 5, 8, 5, 3, 2, 1], 16),
            evans.PitchHandler(
                [
                    -8,
                    0,
                    -8,
                    0,
                    -8,
                    -7,
                    -6,
                    -2,
                    -4,
                    0,
                    1,
                    5,
                    1,
                    5,
                    6,
                    0,
                    8,
                    0,
                    8,
                    -8,
                    8,
                    -8,
                    8,
                    -8,
                    8,
                    -8,
                    8,
                    0,
                    -4,
                ],
                staff_positions=True,
            ),
            evans.zero_padding_glissando,
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", (2, 8)),
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(
                evans.Sequence([3, 4, 5, 4, 6, 3, 6, 7, 3, 2, 7, 8]).derive_intervals(
                    [
                        8,
                        None,
                        6,
                        None,
                        8,
                        9,
                        None,
                        6,
                        9,
                        8,
                        None,
                        6,
                        5,
                        10,
                        5,
                        10,
                        None,
                        5,
                        4,
                        6,
                    ],
                    cyclic=True,
                    match_longest=True,
                )
            ),
            mamu.replace_chords_with_tremolo_containers(
                [1, 1, 1, 2, 1, 3],
                ["up", "up", "down", "up", "down", "up", "down", "down", "down"],
            ),
            evans.NoteheadHandler(
                ["harmonic"],
                head_boolean_vector=[1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            ),
            abjad.Dynamic("ppp"),
            abjad.StartHairpin("<"),
            evans.Attachment(
                abjad.Dynamic("ff"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(
                            r"\markup \upright {non \hspace #0.5 gridato}"
                        ),
                        style=r"solid-line-with-arrow",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(
                            r"\markup \upright {molto \hspace #0.5 gridato}"
                        ),
                        style=r"solid-line-with-arrow",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.select.leaf(_, -4),
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(
                            r"\markup \upright {non \hspace #0.5 gridato}"
                        ),
                        style=r"dashed-line-with-hook",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(_, -4),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [9, 10]),
            evans.note(),
            evans.PitchHandler(motif_sequence),
            # evans.AfterGraceContainer([abjad.Note(8, (1, 16))], with_glissando=True, hide_accidentals=True, position=7),
            lambda _: [abjad.detach(abjad.Tie(), abjad.select.leaf(_, 0))],
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(
                    6, 7, 6, 6, 5, 5, 4, 3, 5, 2, 1, right_padding=0.5, match=True
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            evans.Attachment(
                evans.AfterGraceContainer(
                    [abjad.Note(13, (1, 16))],
                    with_glissando=True,
                    hide_accidentals=True,
                    position=7,
                ),
                selector=lambda _: abjad.select.leaf(_, 2, grace=False),
            ),
            evans.Attachment(
                abjad.Glissando(),
                selector=lambda _: abjad.select.leaf(_, 2, grace=False),
            ),
            evans.Attachment(
                evans.make_fancy_gliss(
                    7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, right_padding=0.5, match=True
                ),
                selector=lambda _: abjad.select.leaf(_, 2, grace=False),
            ),
            abjad.Dynamic("ff"),
            evans.ArticulationHandler(
                ["accent"], articulation_boolean_vector=[1, 0, 1]
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [11, 12, 13]),
            evans.talea([8, 5, 3, 2, 1, 1, 1, 2, 3, 5], 8),
            evans.loop([26], [-3]),
            evans.zero_padding_glissando,
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(r"\trem-two-markup"),
                        style=r"solid-line-with-arrow",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.select.leaf(_, -4),
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(r"\trem-four-markup"),
                        style=r"dashed-line-with-hook",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(_, -4),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            abjad.Dynamic("mp"),
            abjad.StartHairpin("<|"),
            evans.Attachment(
                abjad.Dynamic("fff"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [15, 16, 17]),
            evans.talea(
                [31, 23],
                16,
                extra_counts=[0, 1, 2, 3],
                preprocessor=evans.make_preprocessor(quarters=True),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([0, 6], 7)
                        )
                    ),
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.logical_ties(_), abjad.index([0, 14], 15)
                        )
                    ),
                ],
            ),
            evans.PitchHandler(
                evans.Sequence([3, 4]).derive_intervals(
                    [8, 6], cyclic=True, match_longest=True
                )
            ),
            mamu.replace_chords_with_tremolo_containers([1, 1], ["down", "up"]),
            evans.Attachment(
                abjad.StartHairpin("o<"),
                selector=lambda _: abjad.select.leaf(_, 0, pitched=True),
            ),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, 3, pitched=True),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(_, 3, pitched=True),
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.select.leaf(_, 5, pitched=True),
            ),
            evans.Attachment(
                abjad.StartHairpin("o<"),
                selector=lambda _: abjad.select.leaf(_, 6, pitched=True),
            ),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, 8, pitched=True),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(_, 8, pitched=True),
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.select.leaf(_, 9, pitched=True),
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(r"\markup \upright T"),
                        style=r"dashed-line-with-hook",
                        command=r"\startTextSpanOne",
                    ),
                    r"\tweak staff-padding #5.5",
                    # r"\tweak bound-details.right.padding #3",
                ),
                selector=lambda _: abjad.select.leaf(_, 0, pitched=True),
            ),
            evans.Attachment(
                abjad.StopTextSpan(command=r"\stopTextSpanOne"),
                selector=lambda _: abjad.get.leaf(
                    abjad.select.leaf(_, -1, pitched=True), 1
                ),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", (19, 27)),
            evans.talea(
                evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(),
                16,
                preprocessor=evans.make_preprocessor(quarters=True),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([4, 7, 8], 9)
                        )
                    ),
                ],
            ),
            evans.PitchHandler(
                evans.Sequence(
                    [0, 7 + 1, 7 + 7 + 2, 7 + 7 + 7 + 3]
                ).derive_added_sequences(
                    evans.Sequence.range(
                        abjad.NamedPitch("g").number, abjad.NamedPitch("g''"), 1
                    ).random_walk(
                        length=60,
                        random_seed=9252024641,
                        step_list=evans.Sequence([1, 2, 3, 4, 5, 6])
                        .random_sequence(random_seed=9252024642)
                        .stutter([3, 2, 3, 4, 3, 5, 2]),
                    )
                )
            ),
            evans.zero_padding_glissando,
            lambda _: [mamu.swells(run) for run in abjad.select.runs(_)],
        ),
        evans.MusicCommand(
            ("change voice", (19, 27)),
            evans.even_division(
                [32, 32, 16, 32, 16, 16],
                extra_counts=evans.Sequence([0, -3, 1, -2, 2, -1, 3]).mirror(
                    sequential_duplicates=False
                ),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([4, 7, 8], 9)
                        )
                    ),
                ],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                mamu.string_crossing_modules(first_state=0, random_seed=29, length=60),
                staff_positions=True,
            ),
            *cutaway_commands,
            evans.slur(
                mamu.string_crossing_modules(
                    first_state=0, random_seed=29, length=60, return_lengths_only=True
                )
            ),
            evans.text_span(
                [
                    r"\diamond-notehead-markup",
                    r"\default-notehead-markup",
                    r"\half-diamond-notehead-markup",
                ],
                "->",
                [10],
                padding=6,
                id=3,
            ),
            evans.text_span(
                ["P", "T", "N", "P", "T", "N"], "->", [8], padding=7.5, id=2
            ),
        ),
        evans.MusicCommand(
            ("violin voice", (27, 33)),
            evans.talea(
                evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(),
                16,
                preprocessor=evans.make_preprocessor(quarters=True),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([4, 7, 8], 9)
                        )
                    ),
                ],
            ),
            evans.loop([27, 23, 18, 26, 22, 18, 14], [-4, -5, -6]),
            evans.zero_padding_glissando,
            trem_swell,
        ),
        evans.MusicCommand(
            ("violin voice", [33]),
            evans.talea(
                evans.Sequence([4, 3, 2, 1]).zipped_bifurcation(),
                16,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.loop([abjad.NamedPitch("g").number], [12]),
            lambda _: evans.upward_gliss(_, zero_padding=True),
            # trem_swell,
            abjad.Dynamic("sfp"),
            abjad.StartHairpin("<"),
        ),
        evans.MusicCommand(
            ("violin voice", (34, 42)),
            evans.talea(
                evans.Sequence([4, 3, 2, 1]).random_sequence(
                    random_seed=9262024750, total_length=40
                ),
                32,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            # evans.PitchHandler([30]),
            evans.PitchHandler([motif_sequence.rotate(2).transpose(12)[0]]),
            evans.ArticulationHandler(
                ["accent"],
                articulation_boolean_vector=[
                    1,
                    0,
                    0,
                    1,
                    0,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                ],
            ),
            abjad.Dynamic("fff"),
            abjad.Clef("treble^8"),
        ),
        evans.MusicCommand(
            ("violin voice", (43, 47)),
            evans.talea(
                evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(),
                16,
                preprocessor=evans.make_preprocessor(quarters=True),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([-4, -7, -8], 9)
                        )
                    ),
                ],
            ),
            evans.PitchHandler(
                evans.Sequence(
                    [0, 7 + 1, 7 + 7 + 2, 7 + 7 + 7 + 3]
                ).derive_added_sequences(
                    evans.Sequence.range(
                        abjad.NamedPitch("g").number, abjad.NamedPitch("g''"), 1
                    ).random_walk(
                        length=60,
                        random_seed=9262024809,
                        step_list=evans.Sequence([1, 2, 3, 4, 5, 6])
                        .random_sequence(random_seed=9262024809)
                        .stutter([3, 2, 3, 4, 3, 5, 2]),
                    )
                )
            ),
            evans.zero_padding_glissando,
            lambda _: [mamu.swells(run) for run in abjad.select.runs(_)],
            abjad.Clef("treble"),
        ),
        evans.MusicCommand(
            ("change voice", (43, 47)),
            evans.even_division(
                [32, 32, 16, 32, 16, 16],
                extra_counts=evans.Sequence([0, -3, 1, -2, 2, -1, 3]).mirror(
                    sequential_duplicates=False
                ),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([-4, -7, -8], 9)
                        )
                    ),
                ],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                mamu.string_crossing_modules(
                    first_state=1, random_seed=2692024810, length=60
                ),
                staff_positions=True,
            ),
            *cutaway_commands,
            evans.slur(
                mamu.string_crossing_modules(
                    first_state=1,
                    random_seed=2692024810,
                    length=60,
                    return_lengths_only=True,
                )
            ),
            evans.text_span(
                [
                    r"\diamond-notehead-markup",
                    r"\default-notehead-markup",
                    r"\half-diamond-notehead-markup",
                ],
                "->",
                [10],
                padding=6,
                id=3,
            ),
        ),
        evans.MusicCommand(
            ("bow voice", (48, 80)),
            evans.accelerando(
                [(1, 8), (1, 13), (1, 16)],
                [(1, 8), (1, 12), (1, 16)],
                [(1, 14), (1, 7), (1, 16)],
                [(1, 11), (1, 7), (1, 16)],
                [(1, 8), (1, 17), (1, 16)],
                [(1, 8), (1, 16), (1, 16)],
                [(1, 15), (1, 8), (1, 16)],
                preprocessor=evans.make_preprocessor(
                    sum=True,
                    quarters=True,
                    fuse_counts=[3, 3, 4, 3, 2, 4],
                    split_at_measure_boundaries=True,
                ),
            ),
            evans.zero_padding_glissando,
            evans.bcp(
                [
                    "0/9",
                    "1/9",
                    "2/9",
                    "3/9",
                    "4/9",
                    "5/9",
                    "6/9",
                    "7/9",
                    "8/9",
                    "9/9",
                    "8/9",
                    "7/9",
                    "6/9",
                    "5/9",
                    "4/9",
                    "3/9",
                    "2/9",
                    "1/9",
                ],
                padding=4,
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\stopStaff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(
                    r"\override Staff.StaffSymbol.transparent = ##t", site="after"
                ),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\startStaff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            # evans.slur([9, 5], direction=abjad.UP),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", (48, 79)),
            evans.talea(
                evans.Sequence([11, 10, 9, 8, 7, 6, 5, 4]).random_sequence(
                    random_seed=26, total_length=200
                ),
                16,
                extra_counts=evans.Sequence([0, 1, 2, 3])
                .random_sequence(random_seed=26, total_length=200)
                .remove_repeats(),
                preprocessor=evans.make_preprocessor(quarters=True),
                # rewrite=-1,
                # treat_tuplets=True,
            ),
            evans.PitchHandler(
                evans.Sequence.range(
                    abjad.NamedPitch("g").number, abjad.NamedPitch("g'''").number, 0.5
                )
                .mirror(sequential_duplicates=False)
                .rotate(6)
                .random_walk(
                    length=2000,
                    random_seed=3,
                    step_list=evans.Sequence([1, 2, 3])
                    .random_sequence(total_length=20)
                    .stutter([2, 3, 1, 4, 3]),
                )
            ),
            evans.zero_padding_glissando,
            mamu.swells,
            evans.text_span(
                ["P", "1/2 P", "T", "1/2 T", "T", "XT"], "->", [8], padding=4.5, id=2
            ),
            evans.text_span(
                [
                    r"\diamond-notehead-markup",
                    r"\default-notehead-markup",
                    r"\half-diamond-notehead-markup",
                ],
                "->",
                [10],
                padding=6.5,
                id=3,
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [79]),
            evans.talea(
                [5, 2, 4, 3],
                8,
            ),
            evans.PitchHandler(motif_sequence),
            evans.TranspositionHandler([12, 0, -12, 0]),
            abjad.Dynamic("fff"),
        ),
        evans.MusicCommand(
            ("violin voice", [81]),
            evans.talea(
                [5, 2, 4, 3],
                8,
            ),
            evans.PitchHandler(motif_sequence),
            evans.TranspositionHandler([12, 0, -12, 0]),
            abjad.Dynamic("fff"),
            evans.Attachment(
                abjad.Markup(r"\markup \upright {molto gridato}"),
                selector=lambda _: abjad.select.leaf(_, 0),
                direction=abjad.UP,
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [82]),
            evans.note(),
            evans.PitchHandler(motif_sequence.rotate(3)),
            evans.TranspositionHandler(evans.Sequence([12, 0, -12, 0]).rotate(3)),
            rmakers.untie,
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(
                    9,
                    9,
                    9,
                    9,
                    9,
                    8,
                    8,
                    8,
                    7,
                    7,
                    6,
                    5,
                    4,
                    3,
                    2,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    right_padding=0.5,
                    match=True,
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            abjad.Dynamic("sff"),
            abjad.StartHairpin(">o"),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.get.leaf(
                    abjad.select.leaf(_, -1),
                    1,
                ),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [84]),
            evans.note(),
            evans.PitchHandler(motif_sequence.rotate(0)),
            evans.TranspositionHandler(evans.Sequence([12, 0, -12, 0]).rotate(0)),
            rmakers.untie,
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(
                    9,
                    9,
                    9,
                    9,
                    9,
                    8,
                    8,
                    8,
                    7,
                    7,
                    6,
                    5,
                    4,
                    3,
                    2,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    right_padding=0.5,
                    match=True,
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            abjad.Dynamic("sff"),
            abjad.StartHairpin(">o"),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.get.leaf(
                    abjad.select.leaf(_, -1),
                    1,
                ),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [86, 87]),
            evans.note(),
            evans.PitchHandler(motif_sequence.rotate(0)),
            evans.TranspositionHandler(evans.Sequence([12, 0, -12, 0]).rotate(0)),
            rmakers.untie,
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(
                    9,
                    9,
                    9,
                    9,
                    9,
                    8,
                    8,
                    8,
                    7,
                    7,
                    6,
                    5,
                    4,
                    3,
                    2,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    3,
                    3,
                    3,
                    3,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    right_padding=0.5,
                    match=True,
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            abjad.Dynamic("sff"),
            abjad.StartHairpin(">o"),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.select.leaf(_, 1),
            ),
            evans.Attachment(
                abjad.Glissando(), selector=lambda _: abjad.select.leaf(_, 2)
            ),
            evans.Attachment(
                evans.make_fancy_gliss(
                    9,
                    9,
                    9,
                    9,
                    9,
                    8,
                    8,
                    8,
                    7,
                    7,
                    6,
                    5,
                    4,
                    3,
                    2,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    4,
                    4,
                    1,
                    1,
                    1,
                    1,
                    1,
                    6,
                    6,
                    6,
                    1,
                    1,
                    2,
                    2,
                    1,
                    1,
                    right_padding=0.5,
                    match=True,
                ),
                selector=lambda _: abjad.select.leaf(_, 2),
            ),
            evans.Attachment(
                abjad.Dynamic("sff"), selector=lambda _: abjad.select.leaf(_, 2)
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"), selector=lambda _: abjad.select.leaf(_, 2)
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.select.leaf(_, 3),
            ),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [88]),
            evans.talea(
                evans.Sequence([5, 2, 4, 3]).rotate(2),
                8,
            ),
            evans.PitchHandler(motif_sequence.rotate(2)),
            evans.TranspositionHandler(evans.Sequence([12, 0, -12, 0]).rotate(2)),
            abjad.Dynamic("fff"),
            # evans.Attachment(
            #     abjad.Markup(r"\markup \upright {molto gridato}"),
            #     selector=lambda _: abjad.select.leaf(_, 0),
            #     direction=abjad.UP,
            # ),
        ),
        evans.MusicCommand(
            ("violin voice", (90, 96)),
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.loop([0, 1, 2, 3], [1, 2, -1, 3, -1]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.slur([4]),
            evans.text_span(
                [r"\diamond-notehead-markup", r"\default-notehead-markup"],
                "->",
                [4],
                padding=4.5,
                id=1,
            ),
            evans.text_span([r"non gridato", r"gridato"], "->", padding=6.5, id=2),
            evans.text_span([r"½ clt."], "=|", padding=8.5, id=3),
            evans.hairpin("p < f >", [4]),
        ),
        evans.MusicCommand(
            ("violin voice", (96, 99)),
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(lament_stops),
        ),
        evans.MusicCommand(
            ("violin voice", (100, 103)),
            evans.talea(
                evans.Sequence(
                    evans.Sequence([3, 8, 4, 8, 6]).permutations().flatten(depth=-1)
                ),
                16,
                extra_counts=[0],
                preprocessor=evans.make_preprocessor(
                    eighths=True, fuse_counts=[3], split_at_measure_boundaries=True
                ),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(abjad.select.tuplets(_), abjad.index([2]))
                    ),
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.logical_ties(_, pitched=True),
                            abjad.index([2, 4, 6]),
                        )
                    ),
                ],
                # rewrite=-1,
            ),
            evans.PitchHandler(lament_stops),
            evans.text_span([r"T"], "=|", padding=5.5, id=3),
            evans.text_span([r"non gridato", "molto gridato"], "->", padding=7.5, id=2),
            abjad.Dynamic("ff"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\interrupt", site="before"),
                selector=lambda _: abjad.select.leaf(_, 2, pitched=True),
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\interrupt", site="before"),
                selector=lambda _: abjad.select.leaf(_, 4, pitched=True),
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\interrupt", site="before"),
                selector=lambda _: abjad.select.leaf(_, 7, pitched=True),
            ),
        ),
        evans.MusicCommand(
            ("temporary voice", (100, 103)),
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([0, 1, 3]).permutations().flatten(depth=-1),
                preprocessor=evans.make_preprocessor(
                    eighths=True, fuse_counts=[2], split_at_measure_boundaries=True
                ),
                pre_commands=[
                    lambda _: rmakers.force_rest(
                        abjad.select.get(
                            abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12])
                        )
                    ),
                    lambda _: rmakers.force_rest(
                        [
                            abjad.select.get(
                                abjad.select.leaves(run), abjad.index([0, -1])
                            )
                            for run in abjad.select.runs(_)
                        ]
                    )
                    # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                ],
                # rewrite=-1,
            ),
            evans.loop([_ + 2 for _ in [0, 1, 2, 3, 4]], [1, 2, -1, 3, -1]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.ArticulationHandler(["tremolo"]),
            abjad.Dynamic("pp"),
            evans.text_span([r"molto P"], "=|", padding=5.5, id=3),
            evans.text_span([r"flautando"], "=|", padding=7.5, id=2),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", (156, 160)),
            evans.talea(
                evans.Sequence([5, 2, 4, 3]).rotate(2),
                8,
            ),
            evans.PitchHandler(motif_sequence.rotate(2)),
            evans.TranspositionHandler(evans.Sequence([12, 0, -12, 0]).rotate(2)),
            abjad.Dynamic("fff"),
            evans.Attachment(
                abjad.Markup(r"\markup \upright {molto gridato}"),
                selector=lambda _: abjad.select.leaf(_, 0),
                direction=abjad.UP,
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [104]),
            evans.tuplet([(3, 1)]),
            evans.PitchHandler(motif_sequence),
            abjad.Glissando(),
            evans.Attachment(
                evans.make_fancy_gliss(6, 5, 3, 1, right_padding=0.5, match=True),
                selector=lambda _: abjad.select.leaf(_, 0),
            ),
            abjad.Dynamic("sff"),
            abjad.StartHairpin(">o"),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
            abjad.LilyPondLiteral(r"^\markup \upright {gridato}", site="after"),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.get.leaf(
                    abjad.select.leaf(_, -1),
                    1,
                ),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", (105, 113)),
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
                # pre_commands=[
                #     lambda _: rmakers.force_rest(abjad.select.get(abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12]))),
                #     lambda _: rmakers.force_rest([abjad.select.get(abjad.select.leaves(run), abjad.index([0, -1])) for run in abjad.select.runs(_)])
                #     # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                # ],
                # rewrite=-1,
            ),
            evans.loop([_ + 3 for _ in [0, 1, 2, 3, 4, 7, 5]], [1, 2, -1, 3, -1]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.ArticulationHandler(["tremolo"]),
            lambda _: baca.hairpin(_, "p < ff"),
        ),
        evans.MusicCommand(
            ("violin voice", (113, 123)),
            evans.talea(
                [3, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(violent_stops),
            abjad.Dynamic("fff"),
        ),
        evans.MusicCommand(  # here
            ("violin voice", [123, 124]),  # stops 1
            evans.talea(
                [3, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(violent_stops),
            abjad.Dynamic("fff"),
            abjad.StartHairpin(">"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [125]),  # trem 2
            evans.make_tied_notes(),
            evans.PitchHandler(evans.Sequence([27, 23, 18, 26, 22, 18, 14]).rotate(0)),
            evans.ArticulationHandler(["tremolo"]),
            abjad.Dynamic("fp"),
            abjad.StartHairpin(">o"),
        ),
        evans.MusicCommand(
            ("violin voice", [126]),  # undae 3
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
                # pre_commands=[
                #     lambda _: rmakers.force_rest(abjad.select.get(abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12]))),
                #     lambda _: rmakers.force_rest([abjad.select.get(abjad.select.leaves(run), abjad.index([0, -1])) for run in abjad.select.runs(_)])
                #     # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                # ],
                # rewrite=-1,
            ),
            evans.loop([_ + 3 for _ in [0, 1, 2, 3, 4, 7, 5]], [1, 2, -1, 3, -1]),
            evans.slur([7]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            lambda _: baca.hairpin(_, "p < ff"),
        ),
        evans.MusicCommand(
            ("violin voice", [127]),  # stops 4
            evans.talea(
                [3, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(violent_stops),
            abjad.Dynamic("ff"),
            abjad.StartHairpin(">"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [128]),  # trills 5
            evans.tuplet([(1, 1, 1, 1, 1)]),
            evans.PitchHandler(
                evans.Sequence([3, 4, 5, 4, 6, 3, 6, 7, 3, 2, 7, 8]).rotate(0)
            ),
            evans.trill(
                counts=[1],
                cyclic=True,
                alteration="P4",
                harmonic=True,
                padding=2,
                right_padding=0,
            ),
            abjad.StartHairpin("o<"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StopHairpin(), selector=lambda _: abjad.select.leaf(_, -1)
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [129]),  # trem 6
            evans.make_tied_notes(),
            evans.PitchHandler(evans.Sequence([27, 23, 18, 26, 22, 18, 14]).rotate(1)),
            evans.ArticulationHandler(["tremolo"]),
            abjad.Dynamic("fp"),
            abjad.StartHairpin(">o"),
        ),
        evans.MusicCommand(
            ("violin voice", [130, 131]),  # bend ups 7
            evans.talea(
                [1],
                8,
                extra_counts=[1, 0, 2, 1, 3, 2],
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                    fuse_counts=[1, 2, 1, 1, 2],
                    split_at_measure_boundaries=True,
                ),
            ),
            evans.loop([4, 4, 5, 5, 5, 7, 9, 9, 9, 9, 9], [2]),
            evans.BendHandler([2]),
            abjad.Dynamic("f"),
        ),
        evans.MusicCommand(
            ("violin voice", [132]),  # undae 8
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
                # pre_commands=[
                #     lambda _: rmakers.force_rest(abjad.select.get(abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12]))),
                #     lambda _: rmakers.force_rest([abjad.select.get(abjad.select.leaves(run), abjad.index([0, -1])) for run in abjad.select.runs(_)])
                #     # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                # ],
                # rewrite=-1,
            ),
            evans.loop(
                [_ + 3 + 3 for _ in [0, 1, 2, 3, 4, 7, 5, 6]], [1, 2, -1, 3, -1]
            ),
            evans.slur([8]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            lambda _: baca.hairpin(_, "mp < ff"),
        ),
        evans.MusicCommand(
            ("bow voice", [133]),
            evans.talea(
                [2, 4, 1, 5, 3],
                8,
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                ),
            ),
            evans.zero_padding_glissando,
            evans.bcp(
                [
                    "0/9",
                    "1/9",
                    "2/9",
                    "3/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "8/9",
                    "7/9",
                    "6/9",
                ],
                padding=4,
            ),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", [133]),  # melody 9
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(motif_sequence[:5]),
            evans.TranspositionHandler([24, 12, 0, -12]),
            abjad.Dynamic("fff"),
        ),
        evans.MusicCommand(
            ("violin voice", [134]),  # trills 10
            evans.tuplet([(1, 1, 1, 1, 1, 1)]),
            evans.PitchHandler(
                evans.Sequence([3, 4, 5, 4, 6, 3, 6, 7, 3, 2, 7, 8]).rotate(5 - 2)
            ),
            evans.trill(
                counts=[1],
                cyclic=True,
                alteration="P4",
                harmonic=True,
                padding=2,
                right_padding=0,
            ),
            abjad.StartHairpin("o<"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StopHairpin(), selector=lambda _: abjad.select.leaf(_, -1)
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [135]),  # melody 11
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(motif_sequence[:5]),
            evans.TranspositionHandler([24, 12, 0, -12]),
            abjad.Dynamic("fff"),
        ),
        evans.MusicCommand(
            ("bow voice", [135]),
            evans.talea(
                [2, 4, 1, 5, 3],
                8,
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                ),
            ),
            evans.zero_padding_glissando,
            evans.bcp(
                [
                    "0/9",
                    "1/9",
                    "2/9",
                    "3/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "8/9",
                    "7/9",
                    "6/9",
                ],
                padding=4,
            ),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", [136, 137, 138]),  # bend ups 12
            evans.talea(
                [1],
                8,
                extra_counts=[1, 0, 2, 1, 3, 2],
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                    fuse_counts=[1, 2, 1, 1, 2],
                    split_at_measure_boundaries=True,
                ),
            ),
            evans.loop([_ + 6 for _ in [4, 4, 5, 5, 5, 7, 9, 9, 9, 9, 9]], [2]),
            evans.BendHandler([2]),
            abjad.Dynamic("f"),
        ),
        evans.MusicCommand(
            ("violin voice", [139]),  # stops 1
            evans.talea(
                [3, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(violent_stops),
            abjad.Dynamic("f"),
            abjad.StartHairpin(">"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [140]),  # trem 2
            evans.make_tied_notes(),
            evans.PitchHandler(evans.Sequence([27, 23, 18, 26, 22, 18, 14]).rotate(2)),
            evans.ArticulationHandler(["tremolo"]),
            abjad.Dynamic("fp"),
            abjad.StartHairpin(">o"),
        ),
        evans.MusicCommand(
            ("violin voice", [141]),  # undae 3
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
                # pre_commands=[
                #     lambda _: rmakers.force_rest(abjad.select.get(abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12]))),
                #     lambda _: rmakers.force_rest([abjad.select.get(abjad.select.leaves(run), abjad.index([0, -1])) for run in abjad.select.runs(_)])
                #     # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                # ],
                # rewrite=-1,
            ),
            evans.loop(
                [_ + 3 + 6 for _ in [0, 1, 2, 3, 4, 7, 5, 6, 7]], [1, 2, -1, 3, -1]
            ),
            evans.slur([9]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            lambda _: baca.hairpin(_, "mf < ff"),
        ),
        evans.MusicCommand(
            ("violin voice", [142, 143, 144, 145, 146]),  # stops 4
            evans.talea(
                [3, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(violent_stops),
            abjad.Dynamic("mf"),
            abjad.StartHairpin(">"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [147, 148]),  # trill 5
            evans.tuplet([(1, 1, 1, 1, 1, 1, 1)]),
            evans.PitchHandler(
                evans.Sequence([3, 4, 5, 4, 6, 3, 6, 7, 3, 2, 7, 8]).rotate(
                    5 - 2 + 6 - 3
                )
            ),
            evans.trill(
                counts=[1],
                cyclic=True,
                alteration="P4",
                harmonic=True,
                padding=2,
                right_padding=0,
            ),
            abjad.StartHairpin("o<"),
            evans.Attachment(
                abjad.Dynamic("mp"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(
                    _, len(abjad.select.leaves(_)) // 2
                ),
            ),
            evans.Attachment(
                abjad.StopHairpin(), selector=lambda _: abjad.select.leaf(_, -1)
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [149]),  # trem 6
            evans.make_tied_notes(),
            evans.PitchHandler(evans.Sequence([27, 23, 18, 26, 22, 18, 14]).rotate(3)),
            evans.ArticulationHandler(["tremolo"]),
            abjad.Dynamic("fp"),
            abjad.StartHairpin(">o"),
        ),
        evans.MusicCommand(
            ("violin voice", [150]),  # bend ups 7
            evans.talea(
                [1],
                8,
                extra_counts=[1, 0, 2, 1, 3, 2],
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                    fuse_counts=[1, 2, 1, 1, 2],
                    split_at_measure_boundaries=True,
                ),
            ),
            evans.loop([_ + 6 + 6 for _ in [4, 4, 5, 5, 5, 7, 9, 9, 9, 9, 9]], [2]),
            evans.BendHandler([2]),
            abjad.Dynamic("f"),
        ),
        evans.MusicCommand(
            ("violin voice", [151]),  # undae 8
            evans.talea(
                [1],
                16,
                extra_counts=evans.Sequence([3, 1, 2, 0])
                .permutations()
                .flatten(depth=-1),
                preprocessor=evans.make_preprocessor(quarters=True),
                # pre_commands=[
                #     lambda _: rmakers.force_rest(abjad.select.get(abjad.select.tuplets(_), abjad.index([0, 1, 5, 8, 12]))),
                #     lambda _: rmakers.force_rest([abjad.select.get(abjad.select.leaves(run), abjad.index([0, -1])) for run in abjad.select.runs(_)])
                #     # lambda _: rmakers.force_rest(abjad.select.get(abjad.select.logical_ties(_, pitched=True), abjad.index([23]))),
                # ],
                # rewrite=-1,
            ),
            evans.loop(
                [_ + 3 + 9 for _ in [0, 1, 2, 3, 4, 7, 5, 6, 7, 9]], [1, 2, -1, 3, -1]
            ),
            evans.slur([10]),
            abjad.LilyPondLiteral(r"\harmonicsOn", site="before"),
            evans.Attachment(
                abjad.LilyPondLiteral(r"\harmonicsOff", site="after"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            lambda _: baca.hairpin(_, "f < ff"),
        ),
        evans.MusicCommand(
            ("violin voice", [152, 153]),  # melody 9
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(motif_sequence[:5]),
            evans.TranspositionHandler([24, 12, 0, -12]),
            abjad.Dynamic("fff"),
        ),
        evans.MusicCommand(
            ("bow voice", [152, 153]),
            evans.talea(
                [2, 4, 1, 5, 3],
                8,
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                ),
            ),
            evans.zero_padding_glissando,
            evans.bcp(
                [
                    "0/9",
                    "1/9",
                    "2/9",
                    "3/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "8/9",
                    "7/9",
                    "6/9",
                ],
                padding=4,
            ),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("bow voice", (154, 160)),
            evans.talea(
                [2, 4, 1, 5, 3],
                8,
                preprocessor=evans.make_preprocessor(
                    quarters=True,
                ),
            ),
            evans.zero_padding_glissando,
            evans.bcp(
                [
                    "0/9",
                    "1/9",
                    "2/9",
                    "3/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "0/9",
                    "9/9",
                    "8/9",
                    "7/9",
                    "6/9",
                ],
                padding=4,
            ),
            *cutaway_commands,
        ),
        evans.MusicCommand(
            ("violin voice", (154, 160)),
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.PitchHandler(motif_sequence[:5]),
            evans.TranspositionHandler([24, 12, 0, -12]),
            abjad.Dynamic("fff"),
            evans.Attachment(
                abjad.Glissando(),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.Attachment(
                abjad.Dynamic("sp"),
                selector=lambda _: abjad.select.leaf(_, 11),
            ),
        ),
        evans.MusicCommand(
            ("violin voice", [160]),
            evans.talea(evans.Sequence([9, 8, 7, 6, 5, 4, 3]).zipped_bifurcation(), 16),
            evans.loop([2], [14]),
            abjad.Dynamic("sfp"),
            abjad.StartHairpin("<"),
            evans.upward_gliss,
        ),
        evans.MusicCommand(
            ("violin voice", (161, 165)),
            evans.talea(
                evans.Sequence([4, 3, 2, 1]).random_sequence(
                    random_seed=9262024750, total_length=40
                ),
                16,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([31]),
            evans.zero_padding_glissando,
            abjad.Dynamic("ff"),
            abjad.StartHairpin("<"),
            evans.Attachment(
                abjad.Dynamic("ffff"),
                selector=lambda _: abjad.select.leaf(_, -1),
            ),
            evans.ArticulationHandler(
                ["tremolo"],
                articulation_boolean_vector=evans.Sequence(
                    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
                ).zipped_bifurcation(),
            ),
            evans.text_span([r"non gridato", "molto gridato"], "->", padding=2.5, id=1),
            lambda _: evans.vibrato_spanner(
                peaks=[1, 5, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 3],
                wavelengths=[2, 3, 2, 4, 2, 1],
                thickness=0.2,
                divisions=[4, 5, 4, 6],
                counts=[2],
                cyclic=True,
                padding=4.5,
                forget=False,
            )(abjad.select.leaves(_)[9:]),
            abjad.Clef("treble^8"),
        ),
        #### Cleanup
        evans.call(
            "score",
            evans.SegmentMaker.beam_score_without_splitting,
            lambda _: abjad.select.components(_, abjad.Score),
        ),
        evans.call(
            "violin voice",
            rmakers.unbeam,
            evans.select_measures([_ for _ in range(2, 8)]),
        ),
        evans.attach(
            "Global Context",
            mamu.lib.mark_60,
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "Global Context",
            mamu.lib.met_60,
            lambda _: abjad.select.leaf(_, 0),
        ),
        ####
        # evans.call(
        #     "score",
        #     evans.decorate_artificial_harmonic_chords,
        #     selector=lambda _: _,
        # ),
        #### Fermati
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ulongfermata"',
            ),
            evans.select_measures([1], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ushortfermata"',
            ),
            evans.select_measures([8], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ulongfermata"',
            ),
            evans.select_measures([14], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uveryshortfermata"',
            ),
            evans.select_measures([18], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ushortfermata"',
            ),
            evans.select_measures([42], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([47], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([80], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ulongfermata"',
            ),
            evans.select_measures([83], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ushortfermata"',
            ),
            evans.select_measures([85], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uverylongfermata"',
            ),
            evans.select_measures([89], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uveryshortfermata"',
            ),
            evans.select_measures([99], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([103], leaf=1),
            direction=abjad.UP,
        ),
        #### Repeats
        evans.attach(
            "Global Context",
            mamu.start_repeat,
            evans.select_measures([124 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.center_repeat,
            evans.select_measures([126 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat,
            evans.select_measures([127 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat,
            evans.select_measures([128 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #black \box "1"', site="after"
            ),
            evans.select_measures([128 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_blue,
            evans.select_measures([129 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #blue \box "2!"', site="after"
            ),
            evans.select_measures([129 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_blue,
            evans.select_measures([130 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.center_repeat,
            evans.select_measures([131 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #black \box "1"', site="after"
            ),
            evans.select_measures([131 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_blue,
            evans.select_measures([133 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #blue \box "2!"', site="after"
            ),
            evans.select_measures([133 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_red,
            evans.select_measures([134 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #red \box "3!"', site="after"
            ),
            evans.select_measures([134 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_blue,
            evans.select_measures([135 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_red,
            evans.select_measures([136 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat,
            evans.select_measures([137 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat,
            evans.select_measures([140 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #black \box "1"', site="after"
            ),
            evans.select_measures([140 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_blue,
            evans.select_measures([141 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #blue \box "2"', site="after"
            ),
            evans.select_measures([141 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat,
            evans.select_measures([142 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_blue,
            evans.select_measures([143 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat,
            evans.select_measures([148 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #black \box "1"', site="after"
            ),
            evans.select_measures([148 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_blue,
            evans.select_measures([150 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #blue \box "2"', site="after"
            ),
            evans.select_measures([150 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.start_repeat_red,
            evans.select_measures([151 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(
                r'\mark \markup \with-color #red \box "3"', site="after"
            ),
            evans.select_measures([151 - 2], leaf=0),
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat,
            evans.select_measures([152 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_red,
            evans.select_measures([153 - 2], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            mamu.stop_repeat_blue,
            evans.select_measures([155 - 2], leaf=0),
            direction=abjad.UP,
        ),
        ####
        evans.attach(
            "violin voice",
            abjad.Markup(r"\colophon"),
            lambda _: abjad.select.leaf(_, -3),
            direction=abjad.DOWN,
        ),
        evans.attach(
            "Global Context",
            abjad.BarLine("|."),
            evans.select_measures([165], leaf=1),
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uverylongfermata"',
            ),
            evans.select_measures([165], leaf=1),
            direction=abjad.UP,
        ),
    ],
    score_template=mamu.score,
    transpose_from_sounding_pitch=False,
    time_signatures=mamu.signatures_01,
    clef_handlers=None,
    tuplet_bracket_noteheads=False,
    add_final_grand_pause=False,
    score_includes=[
        "abjad.ily",
        "../../build/segment_stylesheet.ily",
    ],
    segment_name="01",
    current_directory=pathlib.Path(__file__).parent,
    cutaway=False,
    beam_pattern="meter",
    beam_rests=True,
    barline="|.",
    rehearsal_mark="",
    fermata="scripts.ufermata",
    with_layout=True,
    mm_rests=False,
    extra_rewrite=False,  # should default to false but defaults to true
    print_clock_time=True,
    color_out_of_range=False,
)

maker.build_segment()
