Parser will parse between 'START' and 'END' token.
Sheet should start with 'bpm:' info.
Parser will automatically calculate one note's duration time based on bpm.

Notes will be presented as,
(tone, beat)

<Tone>
c3 : do. octave 3. 
cs3 : do sharp. octave3.
ef3 : mi flat. octave3. equal to ds3.
rest : No sound.

After parsing, there will be no flat tones.
ef3 will be ds3.
And also, it will consider semitone(half tone).
es3 will be f3.
cf3 will be b2. bs2 will be c3.

<Beat>
Beat is integer, which goes up 1, 2, 4, 8, and so on.
'1' indicates whole note.
'2' indicates half note.
'4' indicates quarter note.

If (merge, 0) command is between two notes,
series of same tone will be merged.

<LINE>
For harmony or background beat,
there can be line.
Each line will be preocessed individually.

<Sheet>
Sheet will consist of bpm, lines.
'lines' is a list of lines
where every line is list of notes.

<Example - butterfly>
START
bpm: 126
LINESTART
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
LINEEND
LINESTART
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
LINEEND
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