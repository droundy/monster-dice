import 'package:flutter/material.dart';

void main() {
  runApp(new DiceApp());
}

class DiceApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Flutter Demo',
      theme: new ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: new Board(),
    );
  }
}

TableRow _die_row(String name) {
  return new TableRow(children: <Widget>[
    new Image.asset('images/${name}-1.png'),
    new Image.asset('images/${name}-2.png'),
    new Image.asset('images/${name}-3.png'),
    new Image.asset('images/${name}-4.png'),
    new Image.asset('images/${name}-5.png'),
    new Image.asset('images/${name}-6.png'),
  ]);
}

class Monster {
  String name;
  int hp;
  int x;
  int y;
  Monster(String this.name, int this.x, int this.y) {
    this.hp = 6;
  }
}

class Board extends StatefulWidget {
  Board({Key key}) : super(key: key);

  @override
  _BoardState createState() => new _BoardState();
}

class _BoardState extends State<Board> {
  List<Monster> monsters = [];

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance
    // as done by the _incrementCounter method above.
    // The Flutter framework has been optimized to make rerunning
    // build methods fast, so that you can just rebuild anything that
    // needs updating rather than having to individually change
    // instances of widgets.
    var squares = new List(6);
    for (var i=0;i<6;i++) {
      squares[i] = new List(6);
      for (var j=0;j<6;j++) {
        squares[i][j] = new Square.empty(i + j & 1 == 1);
      }
    }
    monsters.forEach((m) => squares[m.x][m.y] = new Square(m.name, m.hp));
    return new Center(
        // Center is a layout widget. It takes a single child and
        // positions it in the middle of the parent.
        child: new Column(
                          children: <Widget>[
                                             new Table(children: <TableRow>[new TableRow(children: squares[0]),
                                                                            new TableRow(children: squares[1]),
                                                                            new TableRow(children: squares[2]),
                                                                            new TableRow(children: squares[3])],
                                                       border: new TableBorder.all(width: 3.0),),
                                             new Table(
                                                       children: <TableRow>[_die_row('red'),
                                                                            _die_row('green'),
                                                                            _die_row('blue'),
                                                                            _die_row('purple'),
                                                                            _die_row('black'),
                                                                            ],
                                                       border: new TableBorder.all(width: 3.0),
                                                       ),
                                             ],
                          ));
  }
}

class Square extends StatelessWidget {
  String name;
  int hp;
  Square(String this.name, int this.hp) {
  }
  Square.empty(bool odd) {
    hp = 0;
    if (odd) { hp = -1; }
    name = '';
  }
  @override
  Widget build(BuildContext context) {
    if (hp == 0) {
      return new Image.asset('images/black-0.png');
    }
    if (hp == -1) {
      return new Image.asset('images/red-0.png');
    }
    return new Image.asset('images/${name}-${hp}.png');
  }
}
