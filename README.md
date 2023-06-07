# set
Сервер работает по адресy: 158.160.106.219(хост на yandex.cloud, написан на FastAPI)

Регистрация:
/api/users/create
Request
{"action": "register", "nickname": "papich", "password": "lalala"}
Response
{
  "status": "ok",
  "token": 1550478
}

Логин:
/api/users/login
Request
{"action": "login", "token": 1550478}
Response
{"status": "ok", "message": "OK, you are logged"}


Раздача карт:
/api/users/fetch
Request
{"action": "fetch", "token": 1550478}
Response
{
  "status": "ok",
  "cards": [
    {
      "id": 14,
      "color": 1,
      "fill": 3,
      "shape": 2,
      "count": 2
    },
    {
      "id": 24,
      "color": 1,
      "fill": 1,
      "shape": 3,
      "count": 3
    },
    {
      "id": 59,
      "color": 3,
      "fill": 3,
      "shape": 2,
      "count": 1
    },
    {
      "id": 53,
      "color": 2,
      "fill": 3,
      "shape": 3,
      "count": 3
    },
    {
      "id": 6,
      "color": 1,
      "fill": 1,
      "shape": 3,
      "count": 1
    },
    {
      "id": 40,
      "color": 2,
      "fill": 2,
      "shape": 2,
      "count": 2
    },
    {
      "id": 32,
      "color": 2,
      "fill": 3,
      "shape": 2,
      "count": 1
    },
    {
      "id": 62,
      "color": 3,
      "fill": 3,
      "shape": 3,
      "count": 1
    },
    {
      "id": 55,
      "color": 3,
      "fill": 2,
      "shape": 1,
      "count": 1
    },
    {
      "id": 69,
      "color": 3,
      "fill": 1,
      "shape": 3,
      "count": 2
    },
    {
      "id": 25,
      "color": 1,
      "fill": 2,
      "shape": 3,
      "count": 3
    },
    {
      "id": 27,
      "color": 2,
      "fill": 1,
      "shape": 1,
      "count": 1
    }
  ]
}

Выбор карт:
/api/users/choose
Request
{"action": "choose", "token": 4879267, "cards": [{
      "id": 14,
      "color": 1,
      "fill": 3,
      "shape": 2,
      "count": 2
    },
    {
      "id": 24,
      "color": 1,
      "fill": 1,
      "shape": 3,
      "count": 3
    },
    {
      "id": 59,
      "color": 3,
      "fill": 3,
      "shape": 2,
      "count": 1
    }]}
Response
{
  "status": "error",
  "cards left": 81,
  "points": -1,
  "message": "your chosen cards are not set, try again"
}
