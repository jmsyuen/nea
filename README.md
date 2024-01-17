# nea notes 
https://github.com/jmsyuen/nea

# general td
can remove blind doubling like a cash game as only in tournaments #
remove database
add help menu text
bot strategies, ai
pygame interface

integrating
display functions for:
revealing all cards at end
small narration box for whos turn it is ##creates new box is effort OR ADD small indicator for player's turn
return to menu and save

FIX LATER 2 problems found may be related
sometimes loops checking
sometimes keeps calling 0 value,


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
