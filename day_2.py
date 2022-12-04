from utils import read_input

inpt = read_input("2")
inpt_parsed = [game.split(" ") for game in inpt]

game_scores = {
    "win": 6,
    "draw": 3,
    "loss": 0
}

play_scores = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

#Elf play - your play
rules = {
    ("rock", "rock"): "draw",
    ("rock", "paper"): "win",
    ("rock", "scissors"): "loss",
    ("paper", "rock"): "loss",
    ("paper", "paper"): "draw",
    ("paper", "scissors"): "win",
    ("scissors", "rock"): "win",
    ("scissors", "paper"): "loss",
    ("scissors", "scissors"): "draw",
}

elf_moves = {
    "A": "rock",
    "B": "paper",
    "C": "scissors"
}

def get_first_solution():
    total_score = 0
    player_moves = {
        "X": "rock",
        "Y": "paper",
        "Z": "scissors"
    }
    for game in inpt_parsed:
        result = rules[(elf_moves[game[0]], player_moves[game[1]])]
        total_score += game_scores[result] + play_scores[player_moves[game[1]]]
    return total_score

def get_second_solution():
    total_score = 0
    player_strategy = {
        "X": "loss",
        "Y": "draw",
        "Z": "win"
    }
    
    play_dict = {
        (plays[0], result): plays[1]
        for plays, result in rules.items()
    }

    for game in inpt_parsed:
        result = player_strategy[game[1]]
        play = play_dict[(elf_moves[game[0]], player_strategy[game[1]])]
        total_score += game_scores[result] + play_scores[play]
    return total_score



print(get_first_solution())
print(get_second_solution())