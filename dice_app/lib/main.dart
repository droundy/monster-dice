import 'package:flutter/material.dart';

void main() {
  runApp(new Board());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Flutter Demo',
      theme: new ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see
        // the application has a blue toolbar. Then, without quitting
        // the app, try changing the primarySwatch below to Colors.green
        // and then invoke "hot reload" (press "r" in the console where
        // you ran "flutter run", or press Run > Hot Reload App in
        // IntelliJ). Notice that the counter didn't reset back to zero;
        // the application is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: new MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful,
  // meaning that it has a State object (defined below) that contains
  // fields that affect how it looks.

  // This class is the configuration for the state. It holds the
  // values (in this case the title) provided by the parent (in this
  // case the App widget) and used by the build method of the State.
  // Fields in a Widget subclass are always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => new _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that
      // something has changed in this State, which causes it to rerun
      // the build method below so that the display can reflect the
      // updated values. If we changed _counter without calling
      // setState(), then the build method would not be called again,
      // and so nothing would appear to happen.
      _counter++;
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
    return new Scaffold(
      appBar: new AppBar(
        // Here we take the value from the MyHomePage object that
        // was created by the App.build method, and use it to set
        // our appbar title.
        title: new Text(widget.title),
      ),
      body: new Center(
        // Center is a layout widget. It takes a single child and
        // positions it in the middle of the parent.
        child: new Column(
          // Column is also layout widget. It takes a list of children
          // and arranges them vertically. By default, it sizes itself
          // to fit its children horizontally, and tries to be as tall
          // as its parent.
          //
          // Invoke "debug paint" (press "p" in the console where you
          // ran "flutter run", or select "Toggle Debug Paint" from the
          // Flutter tool window in IntelliJ) to see the wireframe for
          // each widget.
          //
          // Column has various properties to control how it sizes
          // itself and how it positions its children. Here we use
          // mainAxisAlignment to center the children vertically; the
          // main axis here is the vertical axis because Columns are
          // vertical (the cross axis would be horizontal).
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            new Text(
              '${_counter}',
              style: Theme.of(context).textTheme.display1,
            ),
            new Board(),
            new FlatButton(onPressed: _incrementCounter,
                           child: new Image.asset('images/dragon-6.png',
                                                  width: 100.0,
                                                  height: 100.0,)),
            new Table(
                  children: <TableRow>[
                                       new TableRow(children: <Widget>[
                                           new Square('dragon', 1),
                                           new Square('dragon', 1),
                                           new Square('dragon', 1),
                                           new Square.empty(),
                                           new Square.empty(),
                                           new Square('dragon', 3)]),
                    _die_row('dragon'),
                    _die_row('troll'),
                    _die_row('mage'),
                                       ]..addAll(<TableRow>[
                    _die_row('red'),
                    _die_row('green'),
                    _die_row('blue'),
                    _die_row('purple'),
                    _die_row('black'),
                                                           ]),
                  border: new TableBorder.all(width: 3.0),
              ),
          ],
        ),
      ),
      floatingActionButton: new FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: new Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
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
        squares[i][j] = new Square.empty();
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
  Square.empty() {
    hp = 0;
    name = '';
  }
  @override
  Widget build(BuildContext context) {
    if (hp == 0) {
      return new Container(width:50.0, height: 50.0);
    }
    return new Image.asset('images/${name}-${hp}.png');
  }
}
