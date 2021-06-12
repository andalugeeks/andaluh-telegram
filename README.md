# Andaluh Telegram Bot
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Transliterate your spanish to andaluh EPA using this telegram bot. This bot stores user preferences after interacting with the transliteration options.

<img width="800" alt="andaluh-slack about" src="https://github.com/andalugeeks/andaluh-telegram/blob/master/img/andaluhbot.png?raw=true">

## Table of Contents

- [Installation](#installation)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Installation

First install dependencies

You need to setup 3 environment variables to integrate with Telegram:

- `APIURL`: URl for your [andaluh-api](https://github.com/andalugeeks/andaluh-api) instance. You can use ours as well https://api.andaluh.es/epa
- `TOKEN`: Create your bot with [Telegram's BotFather](https://core.telegram.org/bots) to retrieve your TOKEN
- `USERPREF_PATH`: Where to store the user preferences persistence storage

You can use the `.env` file to store them secretely. Use the `.env.example` template:

```
$ cp .env.example .env # and edit the file!
```

Then you can run the bot using the `run.sh` script for development purposes:

```
$ pip3 install -r requirements.txt
$ run.sh
```

Or dockerised, a better option for production deployments:

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
