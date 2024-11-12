import discord
from discord.ext import commands

# Set up the bot with the prefix you prefer
intents = discord.Intents.default()
intents.members = True  # Necessary for member updates

bot = commands.Bot(command_prefix="!", intents=intents)

# Event to trigger when a member joins or when their roles are updated
@bot.event
async def on_member_update(before, after):
    # Get all roles for the user sorted by position (highest role first)
    roles = sorted(after.roles, key=lambda role: role.position, reverse=True)
    
    # Find the highest role with "Owner" in its name
    highest_owner_role = next((role for role in roles if "Owner" in role.name), None)
    
    if highest_owner_role:
        # Format the nickname with the highest role's name
        new_nickname = f"[{highest_owner_role.name}] {after.display_name}"
        
        # Only change nickname if it’s different
        if after.nick != new_nickname:
            try:
                await after.edit(nick=new_nickname)
                print(f"Updated nickname for {after.name} to {new_nickname}")
            except discord.Forbidden:
                print(f"Bot doesn't have permission to change nickname for {after.name}")
            except discord.HTTPException as e:
                print(f"Failed to change nickname: {e}")

# Start the bot (replace 'YOUR_TOKEN_HERE' with your bot token)
bot.run('MTE1MTE4NjY3MjUwNDAxMjg0MA.Gbc6ss.w1Rw6eRPvVj0FP92UP1uxA6jhpqlqXvoc-DsXY')
