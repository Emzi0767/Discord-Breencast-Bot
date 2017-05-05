import os.path
import cmb
import gevent
from disco.bot.plugin import Plugin
from disco.bot.command import CommandEvent
from disco.gateway.events import Ready
from disco.voice import OpusFilePlayable
from disco.voice.player import Player


class CmbBotCommands(Plugin):
    def __init__(self, bot, config):
        super().__init__(bot, config)
        self.breencast = config
        self.playing = False
        self.player = None
        self.files = []
        self.voice_channel = None

    #@Plugin.listen("Ready")
    def breencast_ready(self, event: Ready):
        cmb.log("Breencast is logged in as {}.".format(event.user.name), tag="INSTANCE")

    # Commands
    @Plugin.command("start")
    def breencast_start(self, event: CommandEvent):
        if event.author.id != 181875147148361728:
            return event.msg.reply("✋")

        if self.playing:
            return event.msg.reply("🔊")

        state = event.guild.get_member(event.author).get_voice_state()
        if not state:
            return event.msg.reply("🔈❌")

        try:
            self.voice_channel = state.channel.connect()
        except Exception as e:
            cmb.logex(e, tag="BREENCAST")
            return event.msg.reply("📡❌")

        self.playing = True
        return event.msg.reply("👌")

    @Plugin.command("play")
    def breencast_play(self, event: CommandEvent):
        if event.author.id != 181875147148361728:
            return event.msg.reply("✋")

        if not self.playing:
            return event.msg.reply("🔈❌")

        self.player = Player(self.voice_channel)
        # event.msg.reply("⌛📤")
        event.msg.reply("🔊")

        while self.playing:
            for k in self.breencast:
                breencast = self.breencast[k]

                for fn in breencast["files"]:
                    try:
                        xf = open(os.path.join("breencast", fn), "rb")
                        self.player.queue.put(OpusFilePlayable(xf))
                    except Exception as e:
                        cmb.logex(e, tag="BREENCAST")

            while not self.player.queue.empty():
                gevent.sleep(0.1)

            cmb.log("All playbacks finished, {}...".format("restarting queue" if self.playing else "awaiting disconnect"), tag="BREENCAST")

        self.player.complete.wait()
        del self.player
        return event.msg.reply("🏁")

    @Plugin.command("stop")
    def breencast_stop(self, event: CommandEvent):
        if event.author.id != 181875147148361728:
            return event.msg.reply("✋")

        if not self.playing:
            return event.msg.reply("🔈❌")

        self.player.disconnect()
        self.playing = False
        return event.msg.reply("👌")
