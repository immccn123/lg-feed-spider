"""
这个程序作为全部程序的入口，调用其他 scripts，并捕获异常。
"""

import sys
from tools.logger import HandleLog

logger = HandleLog()

registered_command = ["export", "fetch", "select", "import_v1", "import"]

if len(sys.argv) == 1:
    print("No command selected! Try these command below:")
    for cmd in registered_command:
        print("\t" + cmd)
    sys.exit(1)

if sys.argv[1] in registered_command:
    logger.info(f"Executing script '{sys.argv[1]}'")
    try:
        exec(f"import scripts.{sys.argv[1]}")
    except Exception as e:
        logger.critical("An exception occurred:")
        print(e)
        logger.critical("Aborted.")
        sys.exit(1)
    logger.info(f"Script '{sys.argv[1]}' done.")
    sys.exit(0)
else:
    print("Unknown command. Try these command below:")
    for cmd in registered_command:
        print("\t" + cmd)
    sys.exit(1)
