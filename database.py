from selectors import DefaultSelector, EVENT_READ
from socket import socket
from random import randint as rint



'''
'''

def accept(sock):
    conn, address = sock.accept()   
    conn.setblocking(False)
    sel.register(conn, EVENT_READ)


def read(conn):
    request = conn.recv(1024)
    if not request:
        conn.close() 
    conn.sendall(response(request.decode()).encode())




'''
Delegates work to different functions inside of this file, similar to what's going on in server.py
'''
def response(request: str) -> str:
    func, arg = request.split("=", 1)
    id = int(arg[-1])
    arg = arg[:-1]
    
    if func == "restart":
        clear_all()
        return "void"
    
    elif func == "set_style":
        name, color = arg.split(',')
        set_style(name, color, id)
        return "void"

    elif func == "save_champ":
        print(f"Player {id} registered {func.split(',')[0]} to their team!")
        save(arg, id)
        return "void"

    elif func == "delete_champ":
        remove(arg)
        return "void"
        
    elif func == "save_toall":
        save_toall(arg)
        return "void"
    
    elif func == "clear_all":
        clear_all()         
        return "void"  

    elif func == "get_all":
        return get_all()

    elif func == "get_frompl":
        return get_pl(arg[-1])

    elif func == "get_styles":
        return get_styles()

    elif func == "get_logo":
        return get_logo()

    elif func == "set_rolls":
        set_rolls()
        return "void"
        
    elif func == "get_rolls":
        return get_rolls()
    

    


sel = DefaultSelector()
sock = socket()
sock.bind(("localhost", 12001))
sock.listen()
sock.setblocking(False)
sel.register(sock, EVENT_READ, True)
print("Database is running...")






''''''''''''''''''''





'''
Sets the rolls for both players. It is VITAL that rolls are set only once per round by only a single client!

Note: A 'roll' is a term used for a random selection, one roll may (for example) produce a single 'r' (which represents a rock)
'''
def set_rolls():
    current_selection =''
    
    for id in range(1, 3):
        with open(f'database/active_game/player{id}_selection.csv', 'r') as _in:
            player_list = [el.strip() for el in _in.readlines()][1:]
        
        for round in range(0, 3):
            for champ in player_list:
                r_num = rint(0, 100)
                probs = [int(float(p)*100) for p in champ.split(',')[1:]]
                
                if r_num in range(0, probs[0]-1):
                    current_selection += 'r'
                elif r_num in range(probs[0], probs[1]-1):
                    current_selection += 'p'
                else:
                    current_selection += 's'
            
        current_selection += '+' if len(current_selection)==6 else ''
            

    with open('database/active_game/current_rolls.txt', 'w') as _in:
        _in.write(current_selection)
'''
'''
      
            
'''
Retrieves the current rolls for both players, which will be split later
'''
def get_rolls():
    with open('database/active_game/current_rolls.txt', 'r') as _in:
        return _in.readline()
'''
'''
    
             
'''
Saves a champion to the player's current selection, a champ string is in the format Name,0.32,0.52,0.29 or whatever.
'''
def save(champ_string : str, id : int) -> None:        
    with open(f'database/active_game/player{id}_selection.csv', 'a') as _in:
        _in.write('\n' + champ_string)  
'''
'''


'''
Gets the current active selection for a single GIVEN player
'''
def get_pl(id : int) -> str:                    
    with open(f'database/active_game/player{id}_selection.csv', 'r') as _in:
        fileread = _in.readlines()
    
    return "+".join([line.strip() for line in fileread])
'''
'''


'''
Called at the end of each game to clear player selection
'''
def clear_all() -> None:
    for n in range(1, 3):                        #removes the selections for both, called at the end of each game
        with open(f'database/active_game/player{n}_selection.csv', 'w') as _in:
            _in.write("None,1.0,1.0,1.0")        #a default value is stored in both files as empty files caused an infinite loop, this line is ignored later
'''
'''


'''
Removes a single champion from the main database
'''
def remove(input_champ : str) -> None:
    list_of_champ_strings = get_all().split('+')
    list_of_champ_strings.remove(input_champ)
    
    
    with open("database/champions/champions.csv", 'w') as _in:
        _in.write('None,1.0,1.0,1.0')                  #placeholder allows us to consistently add \n to beginning without problems
        for remaining_champ in list_of_champ_strings:
            _in.write("\n" + remaining_champ.strip())
'''
'''


'''
Adds a single champion to the main database'''
def save_toall(champ : str) -> None:            #saves a champ in the global database
    with open(f'database/champions/champions.csv', 'a') as _in:
         _in.write('\n' + champ)
'''
'''
    
    
'''
Gets all champions from the main database'''
def get_all() -> str:                                
    with open('database/champions/champions.csv', 'r') as _in:
        fileread = _in.readlines()
    return "+".join([line.strip() for line in fileread][1:])
'''
'''
    
    
'''
Saves the style of the player whose client requests it
'''
def set_style(name, color, id) -> None:
    with open('database/profiles/styles.csv', 'r') as _in:
        styles = [el.strip() for el in _in.readlines()]
    
    styles[id-1] = f"{name},{color}"
    
    with open('database/profiles/styles.csv', 'w') as _out:
        for line in styles:
            _out.write(line + "\n")
'''
'''


'''
Gets the styles of both players
'''
def get_styles() -> None:
    with open('database/profiles/styles.csv', 'r') as _in:
        styles = [el.strip() for el in _in.readlines()]
    
    return "+".join(styles)
'''
'''

'''
Misc functions:
'''
def get_logo() -> str:
    with open('database/data/game_logo.txt', 'r') as _in:
        return "".join([el for el in _in.readlines()])   
'''
'''

while True:
    events = sel.select()
    for key, _ in events:
        if key.data:
            accept(key.fileobj)
        else:
            read(key.fileobj)

