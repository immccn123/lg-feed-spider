'''
这个程序作为全部程序的入口，调用其他scripts，并捕获异常。
'''

import sys
from tools.logger import HandleLog

logger = HandleLog()

registered_command = [
    'export',
    'fetch',
    'select',
    'import_v1',
    'import'
]

if len(sys.argv) == 1:
    print('no command selected!try these command below:')
    for cmd in registered_command:
        print('\t'+cmd)
    sys.exit(1)

if sys.argv[1] in registered_command:
    logger.info(f'executing script \'{sys.argv[1]}\'')
    try:
        exec(f'import scripts.{sys.argv[1]}')
    except Exception as e:
        logger.critical('an exception occurred!')
        print(e)
        logger.critical('Aborted.')
        sys.exit(1)
    logger.info(f'script \'{sys.argv[1]}\' done.')
    sys.exit(0)
else:
    print('unknown command!try these command below:')
    for cmd in registered_command:
        print('\t'+cmd)
    sys.exit(1)
