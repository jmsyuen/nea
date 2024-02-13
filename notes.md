## recompiling code
# windows
pyinstaller --onefile main.py
rename exe to PokerVSBots
move exe file out of dist folder into main folder
delete dist and build folder

recompile 7zip archive
right click folder, add to archive 
enable create sfx archive option
compile

# mac
setup vm with mac iso
pip install pyinstaller
pyinstaller --onefile main.py
rename exe
run pyinstaller in mac environment to create executable file
test pygame install script macinstalldependencies





# general td
can remove blind doubling like a cash game as only in tournaments #
remove database
add help menu text
bot strategies, ai
incorporate binomial, rework bot logic



# optional bugs 
blinds double every total_players - 1 rounds
small bug when raising everyone after doesn't match
remove buttons when human bust
straight flush may incorrectly identify if different flushes and straights exist
better to clear and redraw whole game after every round 
set opponents to 6 list out of may break


# common problems with solutions
program freezing
solution - windows needs to know if user can close using the top right x button
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        quit()


# when testing done
remove current_round_player_index = 0
stop play when human ("player_1") out

# td
make design diagram outlining databases # design stage
implement database # and calling functions
implement money system # £50 buy in chips interval bet of 0.5, for aesthetic only can be calculated easily, 5 chips 5,2,1,50 blinds last two 
implement round systems #

calculation of who wins  and splitting pot in draw #

implement bot strategies
    def StartingCombination
        offsuit, pair etc

    implement predictive calculations of next cards, and chances of success multiplied by the payout and already invested amount and remaining chips and risk level and difficulty
including risk, difficulty, how smart they actually are, etc
    risk is the probability of overriding that value for a high pot
Different strategies for different bots chosen at random maybe 2-3 for different difficulty to represent beginner to advanced knowledge of the game
difficulty may be discrete levels in a scale of 1-10, ranges from easiest to hardest inclusive all including the previous difficulties
starting hands probabilities

implement pygame interface with buttons
to add chip images #5000 in intervals of 50, 5 chip types 5,2,1,50 blinds left 2 of dealer

# other
many maths functions like binomial will be used
    all can be done in python, under the same docs as random()
    see the examples for ideas

when implementing weighted chances for risk behaviour
    utilise weighting probabilities provided with built in function
    see random.choices() in python docs + examples

use sqlite3 as serverless and self-contained - design section
    https://realpython.com/python-sql-libraries/#using-python-sql-libraries-to-connect-to-a-database
    https://www.quackit.com/sqlite/tutorial/create_a_relationship.cfm
    https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3

    
add save and load files, parse from database
    can take datetime as filename, but long and may be inconsistent
