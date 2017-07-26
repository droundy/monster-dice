import 'package:flutter/material.dart';

import 'dice.dart';

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
  String moves;
  Monster(String this.name) {
    x = -1;
    y = -1;
    hp = 6;
    moves = all_monsters[this.name];
  }
  bool legalMove(int newx, int newy) {
    if (x < 0 || y < 0) { return true; }
    if (x == newx && y == newy) {
      return false;
    }
    if ((x-newx).abs() > 1 || (y-newy).abs() > 1) {
      return false;
    }
    if (x != newx && y != newy) {
      return moves.contains('*') || moves.contains('x');
    }
    if (x != newx || y != newy) {
      return moves.contains('*') || moves.contains('+');
    }
    return true;
  }
}

class Board extends StatefulWidget {
  Board({Key key}) : super(key: key);

  @override
  _BoardState createState() => new _BoardState();
}

class _BoardState extends State<Board> {
  List<Monster> monsters = [];

  void _ignoreMonster(Monster m, int x, int y) {
  }
  void _handleMonster(Monster m, int x, int y) {
    setState(() {
      monsters.remove(m);
      m.x = x;
      m.y = y;
      monsters.add(m);
    });
  }

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
        squares[i][j] = new Square.empty(i,j, _handleMonster);
      }
    }
    monsters.forEach((m) => squares[m.x][m.y] = new Square(m, _handleMonster));
    return new ConstrainedBox(
        constraints: new BoxConstraints.expand(),
        child: new Column(
            children: <Widget>[
              new Table(children: <TableRow>[new TableRow(children: squares[0]),
                new TableRow(children: squares[1]),
                new TableRow(children: squares[2]),
                new TableRow(children: squares[3])],
                  border: new TableBorder.all(width: 3.0),),
              new Table(
                  children: <TableRow>[
                    new TableRow(children: <Widget>[
                      new Square(new Monster('mage'), _ignoreMonster),
                      new Square(new Monster('archer'), _ignoreMonster),
                      new Square(new Monster('swordsman'), _ignoreMonster),
                      new Square(new Monster('healer'), _ignoreMonster),
                      new Square(new Monster('axeman'), _ignoreMonster),
                      new Square(new Monster('spearman'), _ignoreMonster),
                    ]),
                    _die_row('red'),
                    _die_row('green'),
                    _die_row('blue'),
                    _die_row('purple'),
                    _die_row('black'),
                  ],
                  border: new TableBorder.all(width: 3.0),
                        ),
            ]));
  }
}

class Square extends StatelessWidget {
  Monster monster = null;
  int x;
  int y;
  dynamic handleMonster;
  bool am_odd() {
    return x + y & 1 == 1;
  }
  Square(Monster this.monster, this.handleMonster) {
    x = monster.x;
    y = monster.y;
  }
  Square.empty(int this.x, int this.y, this.handleMonster);

  void _handleMonster(Monster mon) {
    handleMonster(mon, x, y);
  }
  bool _monsterMoveOk(Monster mon) {
    return mon.legalMove(x, y);
  }

  @override
  Widget build(BuildContext context) {
    var background = new Image.asset('images/black-0.png');
    if (am_odd()) background = new Image.asset('images/red-0.png');
    if (monster == null) {
      return new DragTarget<Monster>(
          onAccept: _handleMonster,
          onWillAccept: _monsterMoveOk,
          builder: (BuildContext context, List<Monster> data, List<dynamic> rejected) {
        return background;
      });
    }
    return new Draggable<Monster>(
        data: monster,
        child: new Image.asset('images/${monster.name}-${monster.hp}.png'),
        childWhenDragging: background,
        feedback: new Container(
            width: 50.0,
            height: 50.0,
            child: new Image.asset('images/${monster.name}-${monster.hp}.png')),
        maxSimultaneousDrags: 1,
                                  );
  }
}
