from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
import uvicorn
from random import randint, shuffle


class Player:
    def __init__(self, nickname, token, points) -> None:
        self.nickname: str = nickname
        self.token: int = token
        self.points: int = points


nicknames = []
tokens = []
players = []


cards = []
i = 0
for color in range(1, 4):
    for count in range(1, 4):
        for shape in range(1, 4):
            for fill in range(1, 4):
                cards.append({"id": i, "color": color, "fill": fill, "shape": shape, "count": count})
                i = i + 1
shuffle(cards)

necessary_cards = cards[0:12]


def create_token():
    while True:
        token = randint(1000000, 9999999)
        if token not in tokens:
            tokens.append(token)
            break
    return token


def check_token(token):
    for player in players:
        if player.token == token:
            return True
    return False


def check_nickname(nickname):
    for player in players:
        if player.nickname == nickname:
            return True
    return False


def check_cards(threecards):
    for card in threecards:
        if card not in cards[0:12]:
            return False
    return True


def all_same_or_all_diff(attr1, attr2, attr3):
    if attr1 == attr2 and attr2 == attr3:
        return True
    elif (attr1 != attr2) and (attr2 != attr3) and (attr3 != attr1):
        return True
    else:
        return False


def find_player(token):
    for player in players:
        if player.token == token:
            return player
    return None

def check_set_on_table(table):
    for c1 in range(len(table)):
        for c2 in range(c1 + 1, len(table)):
            for c3 in range(c2 + 1, len(table)):
                card1 = table[c1]
                card2 = table[c2]
                card3 = table[c3]
                cards = [card1, card2, card3]
                if check_set(cards):
                    return True
    return False


def check_set(chosen_cards):
    card1, card2, card3 = chosen_cards[0], chosen_cards[1], chosen_cards[2]
    count_check = all_same_or_all_diff(
        card1["count"], card2["count"], card3["count"])
    color_check = all_same_or_all_diff(
        card1["color"], card2["color"], card3["color"])
    shape_check = all_same_or_all_diff(
        card1["shape"], card2["shape"], card3["shape"])
    fill_check = all_same_or_all_diff(
        card1["fill"], card2["fill"], card3["fill"])
    return count_check and color_check and shape_check and fill_check


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/users/create")
def create_user(data=Body()):
    nickname = data["nickname"]
    if check_nickname(nickname):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "this nickname already exists"}
        )
    else:
        token = create_token()
        player = Player(nickname, token, 0)
        players.append(player)
        return {"status": "ok", "message": f'Congratulations, your token is {token}'}


@app.post("/api/users/login")
def login_user(data=Body()):
    token = data["token"]
    token = int(token)
    if check_token(token):
        return {"status": "ok", "message": "OK, you are logged"}
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "the token is wrong, try again"}
        )


@app.post("/api/users/fetch")
def fetch_cards(data=Body()):
    fetch = data["action"]
    token = int(data["token"])
    if not check_token(token):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "there is no such token"}
        )
    else:
        if (len(cards) > 12):
            while not check_set_on_table(cards[0:12]):
                shuffle(cards)
        return {"status": "ok", "cards": cards[0:12]}


@app.post("/api/users/choose")
def choose_set(data=Body()):
    take_set = data["action"]
    token = int(data["token"])
    chosen_cards = data["cards"]
    selected_player = find_player(token)
    if not check_token(token):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "there is no such token"}
        )
    else:
        if len(chosen_cards) != 3:
            return {"message": "please, choose 3 cards"}
        else:
            if not check_cards(chosen_cards):
                return {"message": "submitted cards not found"}
            else:
                if check_set(chosen_cards):
                    for card in chosen_cards:
                        cards.remove(card)
                    necessary_cards = cards[0:12]
                    selected_player.points += 3
                    return {"status": "ok", "cards left": len(cards), "points": selected_player.points, "message": "it is set"}
                else:
                    selected_player.points -= 1
                    return {"status": "error", "cards left": len(cards), "points": selected_player.points, "message": "your chosen cards are not set, try again"}





@app.get("/api/users")
def get_users():
    return players


@app.get("/api/cards")
def get_cards():
    return cards



if __name__ == "__main__":
    uvicorn.run("main:app", port = 5000, reload=True)
