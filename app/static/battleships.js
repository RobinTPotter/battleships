 var list = ['water','miss','hit','boat']
 for (var r=1;r<11;r++) {
  for (var c=1;c<11;c++) {
   var coord = 'you_c'+c+'r'+r
   var el = document.getElementById(coord)
   var num = (c*10+r)%list.length
   el.className = list[num]
  }
 }
 var board = true
 function swap() {
  board = !board
  if (!board) {
   document.getElementById('myboard').style="display:none"
   document.getElementById('theirboard').style="display:inherit"
  } else {
   document.getElementById('myboard').style="display:inherit"
   document.getElementById('theirboard').style="display:none"
  }
 }
