# Sleepy Will
This bot was created for my public NSFW Discord server called FallBurn [invite](https://discord.gg/4FneHF3eXt) with the
intent to replace most if not all the general purpose bots on my server

---

## Current Commands
### General User Commands
- /slap
- /kill
- /ping
- /urban
- /anonymous confess
- /report
- /help_me
- /hug

### Staff Commands
- /mute
- /kick
- /ban
- /vc mute
- /force nick

### Owner Commands
- /say text
- /say embed

---

## Current and Planned Features
- [ ] Custom leveling system
- [x] Moderation system
- [ ] Auto-moderation system
- [x] Confession system
- [x] Logging system
- [x] Mental health system
- [ ] Message filter
- [x] Self roles

---

## Want to help out with my little project?
You can add my Discord *dogmoore#3261* along with joining FallBurn


### Personal Code Challenge
I have given myself the challenge to do this project without using **ANY** else or elif keywords. I have found this
resulted in more readable code as it has forced me to use functions and objects where an *else* could've been used 
instead. Would I recommend taking this challenge with one of your projects? Absolutely, it forces you to think a bit
further with how you write code, if something needs to be a function, object, or just a few if statements.

#### For Example
Instead of doing this
```python
async def on_ready(self):
    if config["module"]["welcome"]:
        print('Welcome message: ENABLED')
    else:
        print('Welcome message: DISABLED')
    if config["module"]["events"]:
        print('Events: ENABLED')
    else:
        print('Welcome message: DISABLED')
    if config["module"]["commands"]["fun"]:
        print('Commands: fun ENABLED')
    else:
        print('Commands: fun DISABLED')
    if config["module"]["commands"]["anon"]:
        print('Commands: anonymous ENABLED')
    else:
        print('Commands: anonymous DISABLED')
    if config["module"]["commands"]["general"]:
        print('Commands: general ENABLED')
    else:
        print('Commands: general DISABLED')
    if config["module"]["commands"]["admin"]:
        print('Commands: admin ENABLED')
    else:
        print('Commands: admin DISABLED')
```
Then compare that to this
```python
async def on_ready(self):
    def enabled_check(test):
        if test:
            return 'ENABLED'
        return 'DISABLED'
    print('~~~~~~~~~~')
    print(f'Welcome message: {enabled_check(config["module"]["welcome"])}')
    print(f'Events: {enabled_check(config["module"]["events"])}')
    print(f'Commands: fun {enabled_check(config["module"]["commands"]["fun"])}')
    print(f'Commands: anon {enabled_check(config["module"]["commands"]["anon"])}')
    print(f'Commands: general {enabled_check(config["module"]["commands"]["general"])}')
    print(f'Commands: admin {enabled_check(config["module"]["commands"]["admin"])}')
    print('~~~~~~~~~~')
```
This will also allow much easier scaling, an easier time reading and understanding it at a glance, along with easier
maintenance of code!