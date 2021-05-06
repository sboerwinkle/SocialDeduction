# A modular and dead simple website for hosting social deduction games.
No fancy javascript frameworks, or frills, just flask+javascript.

Forked from [Rengang (Angelo) Yang's repo](https://github.com/OnlyOneByte/SocialDeduction).

Requires:
- Python 3
- Flask
- Flaskwtf
- Redis db\*
- A brain.

Notes on Redis: If you're hosting this on Windows, you need the MS supported one. You can skip Redis and use an in-memory solution (at the cost of no persistence between server launches) by setting the environment variable `SOCIAL_CACHE=mem` when running the server.

Semi-Functional Games:
- Secret Hitler (though you need knowledge of the rules)

Currently WIP Games:
- Avalon
- Werewords
- yes.
