# Pokebot

⚠ *DISCLAIMER!* This bot is under construction! Take a look at the TO-DO list to see which features have already been introduced, as well as those that have yet to be implemented.

## What is Pokébot?
Pokébot is a little Discord bot that allows users to catch and collect Pokémon, as well as providing a competitive and most importantly fun experience between players in many ways. 

## Project structure

Source files are located at the `src` folder. The main script is at the root of the folder, and the remaining source files are organized in two folders:
- The `cogs` folder contains the extensions that need to be loaded before starting the bot.
- The `libs` folder holds the main game logic, some helper functions and exception handlers, logging, etc...
A folder called `res` with the log files and local resources will be created at the root of the project before the bot starts.

The SQL scripts that create the database are stored at the `db` folder. Here's the relational schema for the database:

(in progress)

## Deploying

### On your local computer (for development purposes)
You only need to clone the repository and launch the main script:
```
python3 ./src/main
```

### On Heroku
This project can be hosted at Heroku, you only need to install the Jaws MariaDB plugin. The Procfile is at the root at the project folder.

## TO-DO list
- Information commands
  - [x] Get pokémon type information
  - [x] Get pokémon stats information
  - [ ] Get item information
- Game
  - Pokémon game
    - [ ] Pokédex
    - [ ] Items
    - [ ] Experience and evolutions
  - Battle system
    - [x] Battle rooms
    - [ ] PvE battles
    - [ ] PvP battles
    - [ ] Ranking system
  - Hunting system
    - [ ] Hunt a pokémon
    - [ ] Daily and weekly pokémon list
      - [ ] Pokémon rarity (based on base experience)
  - Multiplayer interactions
    - [ ] Battle leaderboard
    - [ ] Pokédex completion leaderboard
    - [ ] Pokémon exchange
- Database
  - [ ] User inventory
  - [ ] User stats
  - [ ] Leaderboards
