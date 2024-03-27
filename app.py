#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("playlist.db")

#functions
def startScreen():
    print("Welcome to your playlist!")
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")
    print("Enter 1 to add more songs or 0 to continue.")
    choice = helper.get_choice([1,0])

    if choice == 1:
        fileName = input("Please give the file name: ")
        new_data_update(fileName)
        print("Done!")

#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update a song
    5. Delete a song
    6. Delete all songs with empty values
    7. Exit''')
    return helper.get_choice([1,2,3,4,5,6,7])

def modify_options():
    print('''Select from the following attributes to modify: 
    1. Song name
    2. Album name
    3. Artist name
    4. Release Date
    5. Explicit
    6. Cancel''')
    return helper.get_choice([1,2,3,4,5,6])

#search for songs by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

# add extra songs at beginning of program
def new_data_update(fileName):
    data = helper.data_cleaner(fileName)
    attribute_count = len(data[0])
    placeholders = ("?,"*attribute_count)[:-1]
    query = "INSERT INTO songs VALUES(" + placeholders + ")"
    db_ops.bulk_insert(query, data)

def prompt_user():
    # prompt user for the title
    songTitle = ""
    songTitle = input("What is the title of the song? ")
    
    # get the songID
    query = '''
        SELECT DISTINCT songID
        FROM songs
        WHERE Name = ?;
        '''
    songID = db_ops.single_attribute_params(query, (songTitle,))[0]
    return songID 

# update song information given the title
def update_song():
    songID = prompt_user()
    query = '''
        UPDATE songs
        SET 
        '''
    
    # get and modify the attribute based off user input
    change = ""
    attributeChoice = modify_options()
    if attributeChoice == 1:
        query += "Name = ?"
        change = input("What would you like to change it to? ")
    if attributeChoice == 2:
        query += "Album = ?"
        change = input("What would you like to change it to? ")
    if attributeChoice == 3:
        query += "Artist = ?"
        change = input("What would you like to change it to? ")
    if attributeChoice == 4:
        query += "releaseDate = ?"
        year = input("What was the year? ")
        month = input("What was the month? (Please put the value as a two digit value: ex. 01) ")
        day = input("What was the day? (Please put the value as a two digit value: ex. 01) ")
        change = year + "-" + month + "-" + day
    if attributeChoice == 5:
        query += "Explicit = ?"
        print("Enter 1 for Explicit and 0 for Safe.")
        answer = helper.get_choice([1,0])
        if answer == 1:
            change = "True"
        else:
            change = "False"
    if attributeChoice == 6:
        print("Update canceled.")
        return
    
    query += " WHERE songID = ?;"
    db_ops.modify_query_params(query, (change, songID))
    print("Done!")

# delete the songs from the database 
def delete_song():
    songID = prompt_user()
    query = '''
        DELETE FROM songs
        WHERE songID = ?;
        '''
    
    db_ops.modify_query_params(query, (songID,))
    print("Done!")

# delete all songs where one value is NULL
def null_remove():
    query = '''
        DELETE FROM songs
        WHERE songID IS NULL OR
        Name IS NULL OR
        Artist IS NULL OR
        Album IS NULL OR
        releaseDate IS NULL OR
        Genre IS NULL OR
        Explicit IS NULL OR
        Duration IS NULL OR
        Energy IS NULL OR
        Danceability IS NULL OR
        Acousticness IS NULL OR
        Liveness IS NULL OR
        Loudness IS NULL;
        '''
    
    db_ops.modify_query(query)
    print("Done!")

#main method
startScreen()

#program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        update_song()
    if user_choice == 5:
        delete_song()
    if user_choice == 6:
        null_remove()
    if user_choice == 7:
        print("Goodbye!")
        break

db_ops.destructor()