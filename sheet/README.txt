Parser will parse between 'START' and 'END' token.(Should add newline after END token)
Sheet should start with 'bpm:' info.
Parser will automatically calculate one note's duration time based on bpm.

Notes will be presented as,
(tone, beat, volume=5)

<Tone>
c3 : do. octave 3.
c3s : do sharp. octave3.
e3f : do flat. octave3. equal to d3s.
rest : No sound.

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

If (MERGE, 0, 0) command is between two notes,
series of same tone will be merged.

If (ITER, notesnum, iternum) command is after notes,
it will iterate notesnum notes before the command for iternum times.

<Volume>
Volume varies between 1 to 10, integer.
Default size volume is 5.
If not indicated, it will be set to default value 5.

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
(chak, 8, 5)
(ITER, 1, 32)
LINEEND
LINESTART
(boom, 4, 5)
(rest, 4, 5)
(ITER, 2, 8)
LINEEND
LINESTART
(rest, 4)
(bamm, 4)
(ITER, 2, 8)
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
(MERGE, 0)
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
(MERGE, 0)
LINEEND
END

<Result - Parser object>
bpm : 126
Line 1 start
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
('chak', 238, 5)
Line 1 end
Line 2 start
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
('boom', 476, 5)
('rest', 476, 5)
Line 2 end
Line 3 start
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
('rest', 476, 5)
('bamm', 476, 5)
Line 3 end
Line 4 start
('g3', 476, 5)
('e3', 476, 5)
('e3', 476, 5)
('rest', 476, 5)
('f3', 476, 5)
('d3', 476, 5)
('d3', 476, 5)
('rest', 476, 5)
('c3', 476, 5)
('d3', 476, 5)
('e3', 476, 5)
('f3', 476, 5)
('g3', 476, 5)
('g3', 476, 5)
('g3', 357, 5)
('rest', 476, 5)
Line 4 end
Line 5 start
('e3', 476, 5)
('c3', 476, 5)
('c3', 476, 5)
('rest', 476, 5)
('f3', 476, 5)
('d3', 476, 5)
('d3', 476, 5)
('rest', 476, 5)
('e3', 476, 5)
('f3', 476, 5)
('g3', 476, 5)
('a3', 476, 5)
('b3', 476, 5)
('b3', 476, 5)
('b3', 476, 5)
Line 5 end