# You're better off without asking
from gevent import monkey


monkey.patch_all()


import json
from cmblauncher import CmbLauncher
from cmb import log, __version__ as __cmb_version__


def main():
    log("Breencast version {} booting".format(__cmb_version__), tag="CMB LDR")

    log("Loading config", tag="CMB LDR")
    with open("config.json", "r") as f:
        cts = f.read()
        tkd = json.loads(cts)

    log("Launching Breencast", tag="CMB LDR")

    args = {"token": tkd["token"]}

    log("Running", tag="CMB LDR")

    try:
        cmb_launcher = CmbLauncher()
        cmb_launcher.run(**args)

    except KeyboardInterrupt:
        pass

    finally:
        log("Shutting down", tag="CMB LDR")

    log("Shutdown finalized", tag="CMB LDR")


if __name__ == "__main__":
    main()
