# Andaluh Telegram Bot
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Transliterate your spanish to andaluh EPA using this telegrma bot.

<img width="459" alt="andaluh-slack about" src="https://github.com/andalugeeks/andaluh-telegram/blob/master/img/andaluhbot.png?raw=true">

## Table of Contents

- [Installation](#installation)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Installation

You need to setup 2 environment variables to integrate with Telegram:

- `APIURL`: URl for your [andaluh-api](https://github.com/andalugeeks/andaluh-api) instance. You can use ours as well https://api.andaluh.es/epa
- `TOKEN`: Create your bot with [Telegram's BotFather](https://core.telegram.org/bots) to retrieve your TOKEN

Running direclty:

```
$ pip install -r requirements.txt
$ APIURL=https://api.andaluh.es/epa TOKEN=GET_YOURS_WITH_TELEGRAM_BOTFATHER python app/andaluhbot.py
```

Or dockerised:

```
$ docker-compose up --build -d
```

## Roadmap

* Add a new command to exaplain how a transliteration is done, rule by rule. For educationan purposes.
* Add a new command to retrieve andalugeeks memes. For fun!

## Support

Please [open an issue](https://github.com/andalugeeks/andaluh-telegram/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.