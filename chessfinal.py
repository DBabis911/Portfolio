"""PHASE 1: Setup Helpers"""

"""Make lists of allowed Chess pieces"""
WHITE_ALLOWED = ["rook", "bishop", "queen"]
BLACK_ALLOWED = ["king", "queen", "rook", "bishop", "knight", "pawn"]

"""Dictonary to limit Black Pieces"""
BLACK_LIMITS = {
    "king": 1,
    "queen": 1,
    "rook": 2,
    "bishop": 2,
    "knight": 2,
    "pawn": 8
}
"""Dictionary for counting Blacks"""
black_counts = {
    "king": 0,
    "queen": 0,
    "rook": 0,
    "bishop": 0,
    "knight": 0,
    "pawn": 0
}

"""Covert numbers to chess coordinates (Turns (3, 5) into "c5")"""
def coord_to_square(file, rank):
    file_letter = "abcdefgh"[file - 1]
    return f"{file_letter}{rank}"

"""Convert chess coordinates to numbers (Turns "c5" into (3, 5))"""
def square_to_coord(square):
    file_letter = square[0].lower() 
    rank = square[1]         

    file_number = "abcdefgh".index(file_letter) + 1

    rank_number = int(rank)

    return file_number, rank_number

"""input validation  (E.g 'H5')"""
def validate_position(square):
    if len(square) != 2: 
        return False
    
    file = square[0].lower() 
    rank = square[1]

    if file not in "abcdefgh":
        return False

    if rank not in "12345678":
        return False
    
    return True

"""Piece name valditaion"""
def validate_piece(piece, allowed_pieces):
    return piece.lower() in allowed_pieces

"""Generate Legal Moves for Rook
   Each direction is a list of squares in order.
"""
def rook_moves(file, rank):
    directions = []

    # Right (file increases)
    dir_right = []
    for f in range(file + 1, 9):
        dir_right.append((f, rank))
    directions.append(dir_right)

    # Left (file decreases)
    dir_left = []
    for f in range(file - 1, 0, -1):
        dir_left.append((f, rank))
    directions.append(dir_left)

    # Up (rank increases)
    dir_up = []
    for r in range(rank + 1, 9):
        dir_up.append((file, r))
    directions.append(dir_up)

    # Down (rank decreases)
    dir_down = []
    for r in range(rank - 1, 0, -1):
        dir_down.append((file, r))
    directions.append(dir_down)

    return directions


"""Generate Legal Moves for the Bishop
   Each direction is a list of squares in order
"""
def bishop_moves(file, rank):
    directions = []

    # Up-Right
    dir_ur = []
    f, r = file + 1, rank + 1
    while f <= 8 and r <= 8:
        dir_ur.append((f, r))
        f += 1
        r += 1
    directions.append(dir_ur)

    # Up-Left
    dir_ul = []
    f, r = file - 1, rank + 1
    while f >= 1 and r <= 8:
        dir_ul.append((f, r))
        f -= 1
        r += 1
    directions.append(dir_ul)

    # Down-Right
    dir_dr = []
    f, r = file + 1, rank - 1
    while f <= 8 and r >= 1:
        dir_dr.append((f, r))
        f += 1
        r -= 1
    directions.append(dir_dr)

    # Down-Left
    dir_dl = []
    f, r = file - 1, rank - 1
    while f >= 1 and r >= 1:
        dir_dl.append((f, r))
        f -= 1
        r -= 1
    directions.append(dir_dl)

    return directions

    
"""Generate Legal Moves for the Queen"""
def queen_moves(file, rank):
    return bishop_moves(file, rank)+rook_moves(file, rank)   
    
"""Dictonary to assign UNICODE to pieces"""
UNICODE_PIECES = {
    ("white", "king"):   "♔",
    ("white", "queen"):  "♕",
    ("white", "rook"):   "♖",
    ("white", "bishop"): "♗",
    ("white", "knight"): "♘",
    ("white", "pawn"):   "♙",

    ("black", "king"):   "♚",
    ("black", "queen"):  "♛",
    ("black", "rook"):   "♜",
    ("black", "bishop"): "♝",
    ("black", "knight"): "♞",
    ("black", "pawn"):   "♟",
}   

"""Create the board-printing function"""
def print_board(board):
    print("\n   A  B  C  D  E  F  G  H")
    print("  ------------------------")

    for rank in range(8, 0, -1):
        row = f"{rank}|"
        for file in range(1, 9):
            if (file, rank) in board:
                piece = board[(file, rank)]
                symbol = UNICODE_PIECES[(piece["color"], piece["type"])]
                row += f" {symbol} "
            else:
                row += " . "
        row += f"|{rank}"
        print(row)

    print("  ------------------------")
    print("   A  B  C  D  E  F  G  H\n")

"""#PHASE 2 — Input & Validation"""

"""User input for the White Piece"""
def parse_white_input():
    while True:
        user_input = input("Select a White Piece (Rook / Bishop / Queen) and position (e.g., 'Queen H5'): ").strip().lower()

        if user_input == "exit":
            print("Exiting program.")
            exit()

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid format. Use: 'piece position'  e.g. 'queen h5'")
            continue

        piece, square = parts

        if not validate_piece(piece, WHITE_ALLOWED):
            print("Invalid piece! Please select Rook, Bishop or Queen.")
            continue

        if not validate_position(square):
            print("Invalid position! Please select between A1 & H8.")
            continue

        return piece, square
   
"""User input for Black pieces"""
def parse_black_input(used_squares):
    user_input = input("Select a Black Piece and position. E.g. 'King F5' or 'done': ").strip().lower()

    if user_input == "exit": 
        print("Exiting program.") 
        exit()

    if user_input == "done":
        return "done"
    
    parts = user_input.split()
    if len(parts) != 2:
        print("Invalid format. Use: 'Piece Position'  e.g. 'King F5'")
        return None
    
    piece, square = parts

    if not validate_piece(piece, BLACK_ALLOWED):
        print("Invalid piece! Please select a valid piece.")
        return None
    
    if black_counts[piece] >= BLACK_LIMITS[piece]:
        print(f"You already added the maximum number of {piece}s. Select a different piece.")
        return None

    if not validate_position(square):
        print("Invalid position! Please select a position between A1 & H8.")
        return None
    
    if square in used_squares:
        print("Square already occupied. Please select a different square.")
        return None

    return piece, square

"""Collect Black pieces from user"""
def collect_black_pieces(white_square):
    black_pieces = []
    used_squares = {white_square}

    while True:
        result = parse_black_input(used_squares)

        if result == "done":
            if len(black_pieces) == 0:
                print("You must enter at least one black piece.")
                continue
            break
        if result is None:
            continue
        
        piece, square = result

        file, rank = square_to_coord(square)  

        black_pieces.append({
            "type": piece,
            "file": file,
            "rank": rank
        })   

        square_display = coord_to_square(file, rank)
        print(f"Black piece stored: {piece.capitalize()} {square_display.upper()}")

        black_counts[piece] += 1

        used_squares.add(square)
    
    return black_pieces

"""PHASE 3 BOARD REPRESENTATION"""

"""Merge White & Black piece Dictionaries"""
def build_board(white_data, black_pieces):
    board = {}

    wf = white_data["file"]
    wr = white_data["rank"]
    wt = white_data["type"]
    board[(wf, wr)] = {"color": "white", "type": wt}

    for bp in black_pieces:
        bf = bp["file"]
        br = bp["rank"]
        bt = bp["type"]
        board[(bf, br)] = {"color": "black", "type": bt}

    return board

"""Create a white piece"""
def create_white_piece():
    piece, square = parse_white_input()
    file, rank = square_to_coord(square)

    print(f"White piece stored: {piece.capitalize()} {square.upper()}")

    return {
        "type": piece,
        "file": file,
        "rank": rank
    }

"""Find Black piece on White piece move list"""
def find_captures(board, white_piece):
    file = white_piece["file"]
    rank = white_piece["rank"]
    piece_type = white_piece["type"]

    """Generate move lists"""
    if piece_type == "rook":
        directions = rook_moves(file, rank)
    elif piece_type == "bishop":
        directions = bishop_moves(file, rank)
    elif piece_type == "queen":
        directions = queen_moves(file, rank)
    else:
        return []
    """Scan each directional move list to find black piece encouter"""   
    captures = []
    for direction in directions:
        for (f, r) in direction:
            if (f, r) in board and board[(f, r)]["color"] == "black":
                captures.append({
                    "type": board[(f, r)]["type"],
                    "file": f,
                    "rank": r
                })
                break

    return captures

"""Main Program Flow"""

"""""Collect White data"""""
white_data = create_white_piece()

"""""Convert & store inputs & coordinates"""""
white_square = coord_to_square(white_data["file"], white_data["rank"])
file, rank = square_to_coord(white_square)
white_data["file"] = file
white_data["rank"] = rank

"""""Collect Black data"""""
black_pieces = collect_black_pieces(white_square)

"""""Build board"""""
board = build_board(white_data, black_pieces)
print_board(board)

"""""Find captures"""""
captures = find_captures(board, white_data)

"""""Show results"""""
if not captures:
    print("No black pieces can be captured.")
else:
    print("White can capture:")
    for piece in captures:
        square = coord_to_square(piece['file'], piece['rank']).upper()
        print(f"- {piece['type'].capitalize()} on {square}")