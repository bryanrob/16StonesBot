# 16StonesBot
CapstoneProject for Spring of 2022
## Summary
This is a simple Discord bot program that can operate multiple instances of Sixteen Stones for your Discord server.

## Setup
This bot will require Python 3 in order to run.  You will also need access to a MariaDB server.  Once you have the prerequisites in order, proceed to the instructions below:
1) Clone this repository to the device you wish to host the bot onto.
2) Install the following dependencies:
  ```
  discord.py
  python-dotenv
  ```
3) Create a new ```token.tkn``` file; paste and save your Discord bot token into it.
4) Create your MariaDB server.
  - Create a database and run the provided .sql files in the ```/migrations/``` folder in the order that they appear.
5) Create a file called ```db.creds``` and save it with the following text (append each line with your database information as needed):
```
Host_IP=
Host_Port=
Account_User=
Account_Password=
Database_Name=
Table_Name=
```
  - If you ran the SQL file from step 4, your table name will be "*main*".
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
- **leaderboard \[sort by\]**
  - Displays the top 5 listings for users in the same server based on the **sort-by** parameter.  Parameters are as follows:
    - **W**: sorts by wins.
    - **L**: Sorts by losses.
    - **R**: Sorts by win-loss ratio.

## Project Developers
- [Jake (phantump)](https://github.com/phantump)
- [Robert (bryanrob)](https://github.com/bryanrob)
- [Adonis Linares-Velasquez (godadonis)](https://github.com/Godadonis)
