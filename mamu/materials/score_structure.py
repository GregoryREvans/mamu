import abjad

score = abjad.Score(
    [
        abjad.Staff(lilypond_type="TimeSignatureContext", name="Global Context"),
        abjad.StaffGroup(
            [
                abjad.Staff(
                    [abjad.Voice(name="string voice")],
                    name="string staff",
                    lilypond_type="VanishingStringStaff",
                ),
                abjad.Staff(
                    [abjad.Voice(name="bow voice")],
                    name="bow staff",
                    lilypond_type="VanishingBowStaff",
                ),
                abjad.StaffGroup(
                    [
                        abjad.Staff(
                            [abjad.Voice(name="violin voice")],
                            name="violin staff",
                        ),
                        abjad.Staff(
                            [abjad.Voice(name="temporary voice")],
                            name="temporary staff",
                            lilypond_type="VanishingStaff",
                        ),
                    ],
                    name="Interruptive Group",
                    lilypond_type="InterruptiveStaffGroup",
                ),
                abjad.Staff(
                    [abjad.Voice(name="change voice")],
                    name="change staff",
                    lilypond_type="VanishingChangeStaff",
                ),
            ],
            name="Staff Group",
        ),
    ],
    name="Score",
)
