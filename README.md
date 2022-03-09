# 16StonesBot
CapstoneProject for Spring of 2022
## Summary
This is a simple Discord bot program that can operate multiple instances of Sixteen Stones for your Discord server.

## Setup
This bot will require Python 3 in order to run.  Once you have that, proceed to the instructions below:
1) Clone this repository to the device you wish to host the bot onto.
2) Install the following dependencies:
  ```
  discord.py
  python-dotenv
  ```
3) Create a new **token.tkn** file; paste and save your Discord bot token into it.

This concludes the setup process.

## Bot Activation
To activate the bot, simply run the **bot.py** file.  If the setup instructions were followed properly, then the bot will run.

## User Instructions
There are numerous commands available in the bot already with many more on the way!

Each command begins with an \[**!**\] prefix.

The most useful ones are as follows:
- **play @\[other_user\]**
  - Starts a new instance with the user who entered the command and the "other user" that was mentioned.
- **take \[row\] \[stones\]**
  - If the user is in a running instance, the player will take the specified amount of **stones** from the specified **row**.
- **quit**
  - If the user is in a running instance, the player will forfeit the game and close the instance.

## Main Developers
- [Jake (phantump)](https://github.com/phantump)
- [Robert (bryanrob)](https://github.com/bryanrob)