import discord
from discord.ext import commands
from discord.ui import View, Button
from flask import Flask
import threading
import os

TOKEN = os.getenv("BOT_TOKEN")
RULES_CHANNEL_ID = 1455045749439070262  # Your rules channel

BANNER_URL = "https://i.ibb.co/Dg7G4V7s.png"  # Optional banner for embeds

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

# ------------------ Rules Embeds ------------------
RULES_EMBEDS = []

# Page 1: General Conduct
embed1 = discord.Embed(
    title="📜 LOS CHAMPS — OFFICIAL RULEBOOK 📜",
    description="*Respect the league. Respect the game. Respect each other.*",
    color=discord.Color.purple()
)
embed1.add_field(
    name="🌐 GENERAL CONDUCT",
    value="✧ Follow Discord ToS at all times.\n"
          "✧ Treat everyone with basic respect.\n"
          "✧ No harassment, hate speech, threats, or slurs.\n"
          "✧ No spamming or disruptive behavior.\n"
          "If it wouldn’t be acceptable in professional esports, it’s not acceptable here.",
    inline=False
)
embed1.set_image(url=BANNER_URL)
RULES_EMBEDS.append(embed1)

# Page 2: Competitive Integrity & Teams
embed2 = discord.Embed(
    title="🎮 COMPETITIVE INTEGRITY",
    color=discord.Color.gold()
)
embed2.add_field(
    name="Rules",
    value="✦ No smurfing, boosting, or DDoS\n"
          "✦ Play only on your main account\n"
          "✦ No match fixing, throwing, or collusion\n"
          "✦ Play to win — always",
    inline=False
)
embed2.add_field(
    name="🧑‍✈️ TEAMS & PLAYERS",
    value="✧ Teams must have 3 registered players (+1 optional sub)\n"
          "✧ Teams are self-managed\n"
          "✧ Captains are responsible for:\n"
          "  • Communication\n"
          "  • Match readiness\n"
          "  • Scheduling cooperation\n"
          "✨ Be reliable and professional",
    inline=False
)
embed2.set_image(url=BANNER_URL)
RULES_EMBEDS.append(embed2)

# Page 3: Match Day & Majors
embed3 = discord.Embed(
    title="📅 MATCH DAY EXPECTATIONS & 🏆 MAJORS",
    color=discord.Color.blurple()
)
embed3.add_field(
    name="Match Day",
    value="✦ Be on time for scheduled matches\n"
          "✦ Check in early and communicate delays\n"
          "✦ Follow series formats (Bo5 / Bo7)\n"
          "✦ Report results accurately\n"
          "⏱️ Repeated lateness/no-shows may result in penalties",
    inline=False
)
embed3.add_field(
    name="Majors & Events",
    value="✧ Majors are optional but encouraged\n"
          "✧ Follow posted brackets & schedules\n"
          "✧ Unsportsmanlike behavior may result in removal\n"
          "✨ Majors are where legacies are made — act accordingly",
    inline=False
)
embed3.set_image(url=BANNER_URL)
RULES_EMBEDS.append(embed3)

# Page 4: Communication & Staff
embed4 = discord.Embed(
    title="🔔 COMMUNICATION & ⚖️ STAFF",
    color=discord.Color.teal()
)
embed4.add_field(
    name="Communication & Pings",
    value="✦ Use channels appropriately\n"
          "✦ Only ping roles when necessary\n"
          "✦ Keep server readable",
    inline=False
)
embed4.add_field(
    name="Staff & Enforcement",
    value="✧ Staff decisions are final\n"
          "✧ Arguing in public won't change rulings\n"
          "✧ Appeals via staff channels or DMs\n"
          "🛡️ Staff exist to protect the league — not to argue",
    inline=False
)
embed4.add_field(
    name="Consequences",
    value="Violations may result in warnings, penalties, suspensions, or removal",
    inline=False
)
embed4.set_image(url=BANNER_URL)
RULES_EMBEDS.append(embed4)

# Page 5: Chat, Strikes, Sportsmanship
embed5 = discord.Embed(
    title="💬 IN-GAME CHAT & ⚠️ STRIKE SYSTEM",
    color=discord.Color.red()
)
embed5.add_field(
    name="Chat Conduct",
    value="✧ No toxic, sarcastic, or disrespectful quick chats\n"
          "✧ No spamming to tilt or provoke opponents\n"
          "🎮 Chat is for communication, not disrespect",
    inline=False
)
embed5.add_field(
    name="Strike System",
    value="✦ 1st Strike — Official warning\n"
          "✦ 2nd Strike — Immediate removal from team\n"
          "✦ 2 Strikes Total = BANNED from all matches\n"
          "NO third chances",
    inline=False
)
embed5.add_field(
    name="Sportsmanship & Final Warning",
    value="✨ Respect opponents & teammates\n"
          "✨ Let gameplay speak, not chat wheel\n"
          "Staff review reports and apply strikes if intent to be toxic is clear\n"
          "||<@&1455054564683153580>||",
    inline=False
)
embed5.set_image(url=BANNER_URL)
RULES_EMBEDS.append(embed5)

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
            await interaction.response.edit_message(embed=RULES_EMBEDS[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(RULES_EMBEDS)-1:
            self.current_page += 1
            await interaction.response.edit_message(embed=RULES_EMBEDS[self.current_page], view=self)

class ShowRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Show Rules", style=discord.ButtonStyle.green)
    async def show_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RulesView(interaction.user.id)
        await interaction.response.send_message(embed=RULES_EMBEDS[0], view=view, ephemeral=True)

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
