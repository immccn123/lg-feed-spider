"""
这个程序作为全部程序的入口，调用其他 scripts，并捕获异常。
"""

import sys

from scripts import fetch
from scripts import export
from scripts import grab_all
from scripts import migrate_v1
from scripts import migrate
from scripts import select

from tools.logger import HandleLog

logger = HandleLog()

registered_command = [
    ("fetch", fetch),
    ("export", export),
    ("grab_all", grab_all),
    ("migrate_v1", migrate_v1),
    ("migrate", migrate),
    ("select", select),
]

if len(sys.argv) == 1:
    print("no command selected! Try these command below:")
    for cmd in registered_command:
        print("\t" + cmd[0])
    sys.exit(1)

for cmd in registered_command:
    if cmd[0] == sys.argv[1]:
        logger.info(f"Executing script '{sys.argv[1]}'")
        try:
            cmd[1].mainloop()
        except KeyboardInterrupt:
            logger.critical("User aborted.")
            logger.critical("Aborted.")
            sys.exit(1)
        except Exception as e:
            logger.critical("An exception occurred:")
            logger.error(str(e))
            logger.critical("Aborted.")
            sys.exit(1)
        logger.info(f"Script '{sys.argv[1]}' done.")
        sys.exit(0)

logger.error("Unknown command! Try these command below:")
for cmd in registered_command:
    logger.info("\t" + cmd[0])
sys.exit(1)
