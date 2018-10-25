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

Tone also can be arbitrary name,
if that tone has been registered already.
The name should be longer than 4.

For comment,
add # in front of token.

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
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
(chak, 8)
LINEEND
LINESTART
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
(boom, 4)
(rest, 4)
LINEEND
LINESTART
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
(rest, 4)
(bamm, 4)
LINEEND
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
(e3, 4)
(c3, 4)
(c3, 4)
(rest, 4)
(f3, 4)
(d3, 4)
(d3, 4)
(rest, 4)
(e3, 4)
(f3, 4)
(g3, 4)
(a3, 4)
(b3, 4)
(b3, 4)
(b3, 4)
(merge, 0)
LINEEND
END

<Result - Parser object>
bpm : 126
Line 1 start
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
('chak', 238)
Line 1 end
Line 2 start
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
('boom', 476)
('rest', 476)
Line 2 end
Line 3 start
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
('rest', 476)
('bamm', 476)
Line 3 end
Line 4 start
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
Line 4 end
Line 5 start
('e3', 476)
('c3', 476)
('c3', 476)
('rest', 476)
('f3', 476)
('d3', 476)
('d3', 476)
('rest', 476)
('e3', 476)
('f3', 476)
('g3', 476)
('a3', 476)
('b3', 476)
('b3', 476)
('b3', 476)
Line 5 end