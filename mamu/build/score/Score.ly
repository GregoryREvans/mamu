\version "2.25.16"  %2.22.1
\language "english" %! LilyPondFile

\include "abjad.ily"
\include "../score_stylesheet.ily"                                      %! LilyPondFile
%{ \include "abjad.ily" %! LilyPondFile %}

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\score{
    <<
        { \include "layout.ly" }
    	{
            \include "01.ly"
    	}
    >>
%{ \midi{} %}
}
