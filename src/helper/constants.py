import discord

FAIL_IMG = "https://raw.githubusercontent.com/ThomasByr/useful-moderator/master/assets/images/fail.png"
HELP_IMG = "https://raw.githubusercontent.com/ThomasByr/useful-moderator/master/assets/images/help.png"
INVITE_IMG = "https://raw.githubusercontent.com/ThomasByr/useful-moderator/master/assets/images/invite.png"
VOTE_IMG = "https://raw.githubusercontent.com/ThomasByr/useful-moderator/master/assets/images/vote.png"

ME_IMG = "https://raw.githubusercontent.com/ThomasByr/useful-moderator/master/assets/images/useful-moderator.png"

LOADING_EMOJI = discord.PartialEmoji(name='loading', id=983470338417516615, animated=True)
SUCCESS_EMOJI = discord.PartialEmoji(name='check_mark', id=1014226765863989391, animated=True)
FAIL_EMOJI = discord.PartialEmoji(name='across', id=1014227632461709383, animated=True)

GEAR_EMOJI = '⚙️'
NUMERIC_EMOJIS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
YESNO_EMOJIS = ['✅', '❌']
TROPHY_EMOJIS = ['🥇', '🥈', '🥉']

LANDING_CHANNEL_ID = 999457471573790880
LVL_UP_CHANNEL_ID = 999449353502593174

# yapf: disable
CLASS_IMAGES = [
  ['Mystique', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395962129534976/loading_classic_pcw.ktx.png'],
  ['Lotus', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395962532175952/loading_awaken_pkww.ktx.png'],
  ['Sura', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395963035488336/loading_awaken_pnm.ktx.png'],
  ['Eclipse', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395963475902505/loading_awaken_ppw.ktx.png'],
  ['Lys', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395963828211752/loading_awaken_psw.ktx.png'],
  ['Lanciere', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395964193128491/loading_awaken_pvw.ktx.png'],
  ['Enchanteresse', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395964675469413/loading_awaken_pww.ktx.png'],
  ['Hashashin', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395964994244698/loading_classic_pam.ktx.png'],
  ['Poing Furieux', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395965740818482/loading_classic_pcm.ktx.png'],
  ['Seigneur du Sabre', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396075652567061/loading_awaken_pkm.ktx.png'],
  ['Mystique', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396076273311804/loading_awaken_pcw.ktx.png'],
  ['Phantasma', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396076587888710/loading_awaken_pdw.ktx.png'],
  ['Fletcher', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396076906647662/loading_awaken_pem.ktx.png'],
  ['Marche Vent', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396077221224479/loading_awaken_pew.ktx.png'],
  ['Destroyer', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396077519032400/loading_awaken_pgm.ktx.png'],
  ['Solaris', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396077934264340/loading_awaken_pgw.ktx.png'],
  ['Berserker', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396078240440331/loading_awaken_phm.ktx.png'],
  ['Faucheuse', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396078555025488/loading_awaken_phw.ktx.png'],
  ['Raven', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396077875531907/loading_classic_phw.ktx.png'],
  ['Musa', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396078211088505/loading_classic_pkm.ktx.png'],
  ['Primrose', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396078647287849/loading_classic_pkww.ktx.png'],
  ['Shai', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396078991233164/loading_classic_plw.ktx.png'],
  ['Ombrage', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396079423242270/loading_classic_pdw.ktx.png'],
  ['Archer', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396079737798686/loading_classic_pem.ktx.png'],
  ['Chasseuse', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396080123695175/loading_classic_pew.ktx.png'],
  ['Corsaire', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396080408899624/loading_classic_pfw.ktx.png'],
  ['Titan', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396080723468308/loading_classic_pgm.ktx.png'],
  ['Gladiateur', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396081017081937/loading_classic_phm.ktx.png'],
  ['Sage', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396086310293524/loading_classic_ppm.ktx.png'],
  ['Nova', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396086645833758/loading_classic_ppw.ktx.png'],
  ['Lahn', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396086947815434/loading_classic_psw.ktx.png'],
  ['Paladina', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396087304343675/loading_classic_pvw.ktx.png'],
  ['Magicienne', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396087644078120/loading_classic_pww.ktx.png'],
  ['Kunoichi', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396087983804477/loading_classic_pnw.ktx.png'],
  ['Reine Louve', 'https://cdn.discordapp.com/attachments/845724200844263427/1002395965380116572/loading_classic_pbw.ktx.png'],
  ['Louve Celeste', 'https://cdn.discordapp.com/attachments/845724200844263427/1002396075967123456/loading_awaken_pbw.ktx.png'],
  ['Drakania', 'https://cdn.discordapp.com/attachments/841351054925758534/1005765966535327765/unknown.png'],
  ['DrakaniaBdo1', 'https://media.discordapp.net/attachments/845724200844263427/1079045798282666147/0bd6ecb156320220727073756368-1.jpg'],
  ['DrakaniaBdo2', 'https://media.discordapp.net/attachments/845724200844263427/1079045798676926597/69eae911bc320220727073729386-1.jpg'],
  # ['DrakaniaBdo3', 'https://cdn.discordapp.com/attachments/1000506839319969942/1033405986624512070/7dac1ae57d720220726043915404-1.jpg'],
  ['Legatus', 'https://cdn.discordapp.com/attachments/841351054925758534/1005766062077394975/unknown.png'],
  ['Yacha', 'https://cdn.discordapp.com/attachments/841351054925758534/1005766271691915326/unknown.png'],
]
# yapf: enable
