from bot import session, Countdown
from datetime import datetime, timedelta
from discord.ext import commands, tasks


class CountdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.countdown_check.start()

    @commands.command(name="countdown", aliases=["cd", "count"], description="A countdown function that dms you when it finishes with the given text.\nUsage:\n!countdown 10 0 \"Pasta cooked\"\nThis command will dm you Pasta cooked in 10 minutes.\nYou might want to repeat this, maybe you want to be reminded of stuff constantly, in order to do this, you can pass another command like so:\n!countdown 0 1 \"10 Pushups every hour\" \"repeat\" \nThis command will dm you every 1 hour 10 Pushups. You can cancell all your countdowns with !cancelcountdowns")
    async def countdown(self, ctx, minutes:int=0, hours:int=1, text:str="", repeats:str= "no repeat"):
        repeats = True if repeats == "repeat" else False
        if (minutes < 0 or hours < 0) or (minutes >= 60 or hours >= 60) or (minutes <=0 and hours <=0):
            await ctx.send("Minutes/Hours must be bigger than 0 and lesser than 60")
            return
        
        cd = Countdown(user_id=ctx.author.id, issued_date=datetime.now(), expires_at=datetime.now() +timedelta(hours=hours, minutes=minutes), text=text, hours=hours, minutes=minutes, repeat=repeats)
        session.add(cd)
        session.commit()
        await ctx.send(f"Countdown created, will dm you in {hours} hours {minutes} minutes, repeat has been set to {repeats}. Be sure to have DMs enabled from this server {ctx.author.mention}")
        
    
    @commands.command()
    async def cancelcountdowns(self, ctx):
        countdowns = session.query(Countdown).filter_by(user_id=ctx.author.id).all()
        for cd in countdowns:
            session.delete(cd)
        session.commit()
        await ctx.send(f"Deleted all of your {ctx.author.mention} countdowns")

    @tasks.loop(seconds=20)
    async def countdown_check(self):
        print("Checking if any of the countdowns are finished...")
        # get all the countdown object whose expired_at attribute is lesser than the current timestamp 
        countdowns = session.query(Countdown).filter(Countdown.expires_at<=datetime.now()).all()
        # now to dm every user
        for cd in countdowns:
            # this will be hella slow if there are a lot of rows in the database
            user = await self.bot.fetch_user(cd.user_id)
            channel = await user.create_dm()
            await channel.send(f"REMINDER!!!\n\n{cd.text}")

            if not cd.repeat:
                session.delete(cd)
                session.commit()
                return

            cd.expires_at = datetime.now() + timedelta(hours=cd.hours, minutes=cd.minutes)
            session.commit()

def setup(bot):
    """Add it to cogs"""
    bot.add_cog(CountdownCog(bot))