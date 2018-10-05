Parser will parse between 'START' and 'END' token.
Sheet should start with 'bpm:' info.
Parser will automatically calculate one note's duration time based on bpm.

Notes will be presented as,
(tone, beat)

<Tone>
c3 : do. octave 3. 
c3s : do sharp. octave3.
e3f : do flat. octave3. equal to d3s.
rest : No sound.

!!! FOR NOW, NO FLAT !!!
!!! FOR NOW, NO HALF TONE !!!

After parsing, there will be no flat tones.
And also, it will consider semitone.
e3s will be f3.
c3f will be b2. b2s will be c3.

<Beat>
Beat is integer, which goes up 1, 2, 4, 8, and so on.
'1' indicates whole note.
'2' indicates half note.
'4' indicates quarter note.

If (merge, 0) command is between two notes,
series of same tone will be merged.


<Example - butterfly>
START
bpm: 126
(g3, 4)
(e3, 4)
(e3, 4)
(rest, 4)
(f3, 4)
(d3, 4)
(d3, 4)
(rest, 4)
(c3, 4)
(d3, 4)
(e3, 4)
(f3, 4)
(g3, 4)
(g3, 4)
(g3, 8)
(merge, 0)
(g3, 16)
(rest, 4)
END

<Result - Parser object>
bpm : 126
('g3', 476)
('e3', 476)
('e3', 476)
('rest', 476)
('f3', 476)
('d3', 476)
('d3', 476)
('rest', 476)
('c3', 476)
('d3', 476)
('e3', 476)
('f3', 476)
('g3', 476)
('g3', 476)
('g3', 357)
('rest', 476)