import os.path
import argparse
import json


class CmbLauncher:
    def __init__(self):
        pass

    def run(self, token=None):
        # local imports
        from cmb import log, logex, CmbBot, CmbBotCommands
        from disco.bot import BotConfig
        from disco.client import ClientConfig, Client

        # load breencast
        log("Loading Breencasts", tag="CMB PCM")
        with open(os.path.join("breencast", "breencast.json"), "r", encoding="utf-8") as f:
            dat = f.read()
        breencast_data = json.loads(dat)
        breencast_dict = {}

        for breencast in breencast_data:
            bcd = {
                "title": breencast["title"],
                "files": breencast["files"]
            }
            breencast_dict[breencast["id"]] = bcd

        # init cmb
        log("Initializing Breencast", tag="CMB")

        ccfg = ClientConfig()
        ccfg.token = token
        cmb_client = Client(ccfg)

        bcfg = BotConfig()
        bcfg.commands_enabled = True
        bcfg.commands_prefix = "cmb:"
        bcfg.commands_require_mention = False
        bcfg.commands_allow_edit = False

        cmb_bot = CmbBot(cmb_client, bcfg)
        cmb_bot.add_plugin(CmbBotCommands, breencast_dict)

        try:
            log("Breencast connecting", tag="INSTANCE")
            cmb_bot.run_forever()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            logex(e, tag="CMB ERR")

        finally:
            log("Breencast died", tag="INSTANCE")


def initialize_cmb(**kwargs):
    cmb_args = kwargs

    core = CmbLauncher()
    core.run(**cmb_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str, dest="token", help="Bot's token", default=None)

    args = parser.parse_args()
    args = vars(args)

    initialize_cmb(**args)
