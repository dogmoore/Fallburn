import bot
import yaml

tokenFile = yaml.load(open("./Configs/bot.yml", "r"), Loader=yaml.FullLoader)

client = bot.Fallburn()
client.run(tokenFile["token"])
