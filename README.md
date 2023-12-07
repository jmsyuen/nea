# nea notes 

# td
make design diagram outlining databases
implement database # and calling functions
implement money system
implement round systems
implement bot strategies
including risk, difficulty etc
calculation of who wins # and splitting pot in draw
implement predictive calculations of next cards, and chances of success multiplied by the payout and already invested amount and remaining chips and risk level and difficulty
difficulty is how smart they actually are
Different strategies for different bots chosen at random maybe 2-3 maybe for different difficulty to represent beginner to advanced knowledge of the game
difficulty may be discrete levels in a scale of 1-10
starting hands probabilities
risk is the probability of overriding that value for a high pot
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
