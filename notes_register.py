from register import Register

notes = [
  ('a3.MOV', 'a3'),
  ('a3s.MOV', 'a3s'),
  ('b3.MOV', 'b3'),
  ('bamm.mp4', 'bamm'),
  ('boom.mp4', 'boom'),
  ('c3.MOV', 'c3'),
  ('c3s.MOV', 'c3s'),
  ('c4.MOV', 'c4'),
  ('chak.mp4', 'chak'),
  ('d3.MOV', 'd3'),
  ('d3s.MOV', 'd3s'),
  ('e3.MOV', 'e3'),
  ('f3.MOV', 'f3'),
  ('f3s.MOV', 'f3s'),
  ('g3.MOV', 'g3'),
  ('g3s.MOV', 'g3s'),
]

for n in notes:
    Register('./origin_note/'+n[0], n[1])
    print(n[0] + 'is registered as' + n[1])
