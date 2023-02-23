import asyncio
import sys
import aiohttp
from prettytable import PrettyTable
from fpl import FPL
import pyodbc



async def main():

    await UpdateTable()
    await idealPicks()


async def UpdateTable():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=PC08212428;'
                          'Database=FPL_Players;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()

    players = await fpl.get_players()

    try:
        print("Dropping players table.")
        cursor.execute('DROP TABLE players')
    except:
        print("Players table didn't exist, will now create.")

    cursor.execute('''
            CREATE TABLE players (
                player_id INT IDENTITY,
                player_first_name nvarchar(50),
                player_second_name nvarchar(50),
                minutes int,
                cost float,
                form float,
                )
                   ''')
    conn.commit()


    playersCount = len(players)
    print ("There are: ", playersCount, " available players.")



    for i in range(playersCount):
        player_firstname = str(players[i].first_name)

        # For those pesky players with apostrophes in their names, looking at you N'Golo Kante
        player_firstname = player_firstname.replace("'", "''")
        player_secondname = str(players[i].second_name)
        player_secondname = player_secondname.replace("'", "''")
        player_minutes = players[i].minutes
        player_cost = players[i].now_cost / 10
        player_form = players[i].form

        command = ('''
                        INSERT INTO players (player_first_name, player_second_name, minutes, cost, form)
                        VALUES ('{0}', '{1}', {2}, {3}, {4})
                        ''')
        command = command.format(player_firstname, player_secondname, player_minutes, player_cost, player_form)
        conn.execute(command)
        conn.commit()
    cursor.close()


    cursor.commit()

if __name__ == "__main__":
    if sys.version_info >= (3, 7):
         # Python 3.7+
         asyncio.run(main())
    else:
         # Python 3.6
         loop = asyncio.get_event_loop()
         loop.run_until_complete(main())