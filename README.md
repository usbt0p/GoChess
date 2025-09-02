# GoChess

GoChess is a set of chess variants played on a normal chessboard, with the addition of a few varying rules such as:

- Board starts empty
- Players can place pieces on their turn instead of moving
- Placing can be limited trought the game, for example with each player having only 10 placements, only being able to place on the first 5 turns, etc.
- Normal chess rules apply otherwise, including check and checkmate
- Some exceptions are still in the works such as limit to pawn placements, catling conditins, placing kings first / last, etc.
- A huge number of variants can be created by combining these rules in different ways, so the possibilities are huge

The aim of this repo is to create a simple and flexible engine that can handle the different rulesets, on-demand creation of variants while no main variants emerge, and to provide a simple interface for playing the game.

> [!NOTE]
> GoChess is a work in progress. After the main engine is complete, the plan is to create an interface and develop a web app for playing the game online.

## Installation and Usage
For now, the usage is limited to CLI tests since the basic logic is still being developed.
Clone the repo and run the CLI with `python3 backend/cli.py`


## Structure

```
.
├── backend
│   ├── src
│   │   ├── domain
│   │   │   ├── entities
│   │   │   ├── exceptions
│   │   │   ├── services
│   │   │   └── value_objects
│   │   └── infrastructure
│   └── tests
│       ├── integration
│       └── unit
└── frontend
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes, or if you are interested and want to participate more actively, email me. 
Also, if you want to "playtest", text me and we can try somehow to play a game!

## TODO's
- [x] domain entities
- [x] values / types
- [x] Piece movement logic
- [ ] special moves logic:
    - [ ] Castling
    - [x] En passant
    - [ ] Promotion
- [ ] piece placement logic
- [ ] movement validators
- [ ] placement validators
- [ ] validators for checks, checkmates, stalemates, promotion, captures

- [ ] Ruleset configuration system 
- [x] CLI for testing
- [ ] More unit tests
- [ ] logging games using algebraic notation
- [ ] time system and clocks

### Future
- [ ] develop s simple gui
- [ ] get api working on localhost
- [ ] Web app for playing online