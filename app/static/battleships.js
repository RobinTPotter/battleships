var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function ping() {
    socket.emit('ping', {'hello': 'there' });
}

//make sure a board can be decorated

function test_board() {
    var list = ['water','miss','hit','boat']
    for (var r=1;r<11;r++) {
        for (var c=1;c<11;c++) {
            var coord = 'you_c'+c+'r'+r
            var el = document.getElementById(coord)
            var num = (c*10+r)%list.length
            el.className = list[num]
        }
    }
}

//test_board()
//to toggle view of board, you or opponent

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

function ready(g) {
    socket.emit('ready', {'game': g});
}

function update_server(boat,g,u) {
    socket.emit('boat_moved', { 'boat': boat, 'game': g, 'user': u } )
}

socket.on('joined', function(data) {
    console.log('welcome '+data.id)
    document.getElementById('opponents_name').innerHTML = data.id
})

socket.on('player_turn_changed', function(data) {
    console.log('player_turn_changed', data.id)
    document.getElementById('whose_turn').innerHTML = '| ' + data.name + '\'s turn'
})

socket.on('stage_changed', function(data) {
    console.log('stage_changed', data.id)
    document.getElementById('game_stage').innerHTML = data.stage
})

socket.on('game_on', function(data) {
    console.log('game on',data)
    document.getElementById('whose_turn').innerHTML = '| ' + data.name + '\'s turn'
})
