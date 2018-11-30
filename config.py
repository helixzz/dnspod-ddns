import os
import getopt
import sys
import logging

# linux
config_path = 'ddnsrc'
# windows
if os.name == 'nt':
    config_path = 'ddnspod.cfg'

cfg = {}
cfg["login_token"] = ''

cfg["sub_domain"] = ''
cfg["domain"] = ''
cfg["interval"] = '5'
cfg["record_id"] = '{auto}'
cfg["current_ip"] = '{auto}'
cfg["email"] = ''

cfg["ip_count"] = '1'
cfg["ip_pool"] = '{auto}'
cfg["last_update_time"] = '{auto}'


def read_config():
    read_config_from_file()
    read_config_from_env()
    read_config_from_argv()


def print_help():
    max_key_len = max([len(key) for key in cfg.keys()])
    print("ddns.py [-h|...]")
    print("Available params: ")
    for name in cfg.keys():
        print('    --%-' + str(max_key_len) + 's <value>' % name)
    print("Current config path is %s" % config_path)


def read_config_from_file():
    try:
        with open(config_path, 'rU') as fp:
            for line in fp:
                pair = [x.strip() for x in line.split('=')]
                if pair[0] and pair[1]:
                    cfg[pair[0].lower()] = pair[1]
    except:
        pass

def read_config_from_env():
    for key in cfg:
        if os.getenv(key) is not None:
            cfg[key] = os.getenv(key)

def read_config_from_argv():
    available_args = [x + "=" for x in cfg.keys()]
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "h", available_args)
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit()
            if opt.startswith('--'):
                pair = [opt[2:], arg]
                if pair[0] and pair[1]:
                    cfg[pair[0].lower()] = pair[1]
    except getopt.GetoptError:
        print_help()
        sys.exit(1)

def save_config():
    try:
        save_config_to_env()
        save_config_to_file()
    except NotImplementedError as err:
        logging.error("FAILED to save config:" + str(err))

def save_config_to_env():
    for key in cfg:
        os.environ[key] = cfg[key]

def save_config_to_file():
    max_key_len = max([len(key) for key in cfg.keys()])
    try:
        with open(config_path, "w+") as f:
            f.writelines([
                ('%-'+str(max_key_len)+'s=%s\n') % (key, cfg[key])
                for key in cfg.keys()
            ])
    except IOError as err:
        logging.error("FAILED to save config to file: " + str(err))

def check_config():
    if not (
            cfg['login_token'] and
            cfg['domain'] and
            cfg['sub_domain']):
        logging.fatal('config error: need login info')
        exit()
    try:
        if not(int(cfg["interval"])):
            logging.fatal('interval error')
            exit()
        if not(int(cfg["ip_count"])):
            logging.fatal('ip_count error')            
            exit()
    except:
        logging.fatal('config error')
        exit()
    logging.info('config checked')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s: %(message)s')
    logging.info("init cfg: %s" % cfg)
    read_config()
    logging.info("read cfg: %s" % cfg)
    check_config()
