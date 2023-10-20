# from cli.cli_new import run_cli

from src.storage.base_kv import BaseKV

if __name__ == "__main__":
    # start_cli()
    # run_cli()
    pass


b = BaseKV("h")

f = b.get("key", list[str | int])
