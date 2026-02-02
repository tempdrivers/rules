import discord
from discord.ext import commands
from discord.ui import View, Button
from flask import Flask
import threading
import os

TOKEN = os.getenv("BOT_TOKEN")
RULES_CHANNEL_ID = 1455045749439070262  # Channel to send initial "Show Rules" button

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------ Keep Alive Web Server ------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    threading.Thread(target=run_web).start()
# ------------------------------------------------------------

# ------------------ Full Rules Pages ------------------
RULES_PAGES = [
    # Page 1
    "## ✦✦✦ 📜 LOS CHAMPS — OFFICIAL RULEBOOK 📜 ✦✦✦ ##\n\n"
    "*Respect the league. Respect the game. Respect each other.*\n\n"
    "**✦✦✦ 🌐 GENERAL CONDUCT 🌐 ✦✦✦**\n\n"
    "✧ All members must follow Discord Terms of Service at all times.\n"
    "✧ Treat everyone with basic respect — players, staff, and spectators.\n"
    "✧ Competitive banter is allowed; harassment, hate speech, threats, or slurs are NOT.\n"
    "✧ No spamming, excessive tagging, or disruptive behavior.\n\n"
    "If it wouldn’t be acceptable in professional esports setting, it’s not acceptable here.\n"
    "✨ If it wouldn’t be acceptable in professional esports setting, it’s not acceptable here.",
    
    # Page 2
    "**✦✦✦ 🎮 COMPETITIVE INTEGRITY 🎮✦✦✦**\n\n"
    "✦ No smurfing, boosting, or DDoS\n"
    "✦ Play only on your main account.\n"
    "✦ No match fixing, throwing, or collusion.\n"
    "✦ Play to win — always.\n\n"
    "🏆 __Los Champs is built on fair competition. Integrity is non-negotiable.__\n\n"
    "**✦✦✦ 🧑‍✈️ TEAMS & PLAYERS 🧑‍✈️ ✦✦✦**\n\n"
    "✧ Teams must have 3 registered players (1 optional substitute).\n"
    "✧ Teams are self-managed — staff does not place players.\n"
    "✧ Captains are responsible for:\n"
    "  • Team communication\n"
    "  • Match readiness\n"
    "  • Scheduling cooperation\n"
    "✨ Be reliable. Be prepared. Be professional.",
    
    # Page 3
    "**✦✦✦ 📅 MATCH DAY EXPECTATIONS 📅 ✦✦✦**\n\n"
    "✦ Be on time for scheduled matches.\n"
    "✦ Check in early and communicate delays immediately.\n"
    "✦ Series formats must be followed (Bo5 / Bo7 where applicable).\n"
    "✦ Results must be reported accurately.\n"
    "⏱️ Repeated lateness or no-shows may result in penalties.\n\n"
    "**✦✦✦ 🏆 MAJORS & EVENTS 🏆 ✦✦✦**\n\n"
    "✧ Majors are optional but highly encouraged.\n"
    "✧ Teams must follow posted brackets and schedules.\n"
    "✧ Unsportsmanlike behavior during Majors may result in removal.\n"
    "✨ Majors are where legacies are made — act accordingly.",
    
    # Page 4
    "**✦✦✦ 🔔 COMMUNICATION & PINGS 🔔 ✦✦✦**\n\n"
    "✦ Use channels for their intended purpose.\n"
    "✦ Only ping roles when appropriate.\n"
    "✦ Do not abuse @mentions.\n"
    "📣 Keep the server clean and readable.\n\n"
    "**✦✦✦ ⚖️ STAFF & ENFORCEMENT ⚖️ ✦✦✦**\n\n"
    "✧ Staff decisions are final.\n"
    "✧ Arguing in public channels will not change rulings.\n"
    "✧ Appeals may be submitted calmly and respectfully via staff channels or DMs.\n"
    "🛡️ Staff exist to protect the league — not to argue.\n\n"
    "**✦✦✦ 🚨 CONSEQUENCES 🚨 ✦✦✦**\n\n"
    "Violations may result in:\n"
    "✦ Warnings\n✦ Match penalties\n✦ Suspensions\n✦ Removal from the league or server\n"
    "Severity depends on the situation.",
    
    # Page 5
    "**✦✦✦ 👑 FINAL NOTE 👑 ✦✦✦**\n\n"
    "✨ Los Champs is a competitive league, not a public ranked lobby.\n"
    "✨ Respect the structure, the players, and the grind.\n"
    "✨ Play hard. Compete fair. Leave your mark.\n\n"
    "**✦✦✦ 💬 IN-GAME CHAT CONDUCT 💬 ✦✦✦**\n\n"
    "✧ Using quick chats like **“What a save!”**, **“Nice one!”**, **“Okay.”**, etc. in a toxic, sarcastic, or disrespectful way is not allowed.\n"
    "✧ Spamming chat to tilt, mock, or provoke opponents or teammates is considered unsportsmanlike behavior.\n"
    "✧ This league is competitive — mental games through toxicity are not skill.\n"
    "🎮 In-game chat should be used for communication, not disrespect.\n\n"
    "**✦✦✦ ⚠️ STRIKE SYSTEM ⚠️ ✦✦✦**\n\n"
    "Violating chat conduct rules results in **STRIKES**:\n"
    "✦ **1st Strike** — Official warning\n"
    "✦ **2nd Strike** — **Immediate removal from your team**\n"
    "✦ **2 Strikes Total** = **BANNED** from all league matches, RLCS games, and scrims\n"
    "There are **NO third chances**.\n\n"
    "**✦✦✦ 🧠 SPORTSMANSHIP RULE 🧠 ✦✦✦**\n"
    "✨ Competitive doesn’t mean toxic\n"
    "✨ Respect opponents and teammates\n"
    "✨ Let your gameplay talk — not your chat wheel\n\n"
    "**✦✦✦ 🚫 FINAL WARNING 🚫 ✦✦✦**\n"
    "Staff review replays and reports.\n"
    "If intent to be toxic is clear, the strike is applied — no debates in public channels.\n\n"
    "||<@&1455054564683153580>||"
]

# ------------------ Views ------------------
class RulesView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.current_page = 0

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(content=RULES_PAGES[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(RULES_PAGES)-1:
            self.current_page += 1
            await interaction.response.edit_message(content=RULES_PAGES[self.current_page], view=self)

class ShowRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Show Rules", style=discord.ButtonStyle.green)
    async def show_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RulesView(interaction.user.id)
        await interaction.response.send_message(content=RULES_PAGES[0], view=view, ephemeral=True)

# ------------------ Send initial button ------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(RULES_CHANNEL_ID)
    if channel:
        await channel.send("Click the button below to view the official rules:", view=ShowRulesView())

# ------------------ Start Bot ------------------
keep_alive()
bot.run(TOKEN)
