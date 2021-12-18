from app.cli_tool import CLI

cli_tool = CLI()

while True:
    cmd = input(">>> ").strip()
    cli_tool.run_command(cmd)
