#!/usr/bin/env python


import argparse
import re
from pathlib import Path

import requests
import yaml


def set_outlet(outlet, action):
    """set_outlet

create the parameters for submission to the HTTP endpoint. if this is
a single port, then return a single value in the dict. if outlet =
all, then iterate through the range of outlets

    """
    q_params = ""
    state = {"off": "0", "on": "1"}

    if outlet == "all":
        for p in range(1, 5):
            key = "p6" + str(p)
            q_params += key + "=" + state[action]
            # trailing '+' signs drive their parser bonkers
            if p < 4:
                q_params += "+"

    else:
        key = "p6" + outlet
        q_params += key + "=" + state[action]

    return q_params


def parse_response(response_txt):
    """parse_response(string) - parse the request response nicely output
the results of the command execution.

    """
    resp = ""

    state = {"0": "off", "1": "on"}
    outlet_status = re.findall("(p6\d=\d)", response_txt)
    if outlet_status:
        resp += "current outlet status\n"
        resp += "-" * 21 + "\n"
        for s in outlet_status:
            p = re.match("p6(\d)=(\d)", s)
            resp += f"outlet: {p.group(1)} power: {state[p.group(2)]}\n"

    return resp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--outlet",
        dest="outlet",
        required=True,
        choices=["1", "2", "3", "4", "all"],
        help="outlet to set the power state on, values: 1-4, all",
    )
    parser.add_argument(
        "-a",
        "--action",
        dest="action",
        required=True,
        choices=["on", "off", "display"],
        help="action to take upon the associated outlet(s)",
    )

    parser.add_argument(
        "--hostname", dest="hostname", help="IP9258 hostname or IP address"
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="configuration file to use instead of the default",
    )

    parser.add_argument(
        "-u",
        "--username",
        dest="http_user",
        help="username for authentication to the IP9258",
    )

    parser.add_argument(
        "-p",
        "--password",
        dest="http_pass",
        help="password for authentication to the IP9258",
    )
    args = parser.parse_args()

    # load default configuration
    config_file = str(Path.home()) + "/.config/botpower.cfg"
    if args.config_file:
        config_file = args.config_file

    with open(config_file) as yaml_file:
        cfg = yaml.load(yaml_file)

    # command line argument overrides
    if args.hostname:
        cfg["hostname"] = args.hostname

    if args.http_user:
        cfg["username"] = args.http_user

    if args.http_pass:
        cfg["password"] = args.http_pass

    print("outlet:", args.outlet)
    print("action:", args.action)

    query_params = ""
    if args.action != "display":
        query_params += "cmd=setpower+"
        query_params += set_outlet(args.outlet, args.action)
    else:
        query_params += "cmd=getpower"

    url = "http://" + cfg["hostname"] + cfg["api_url"] + query_params

    r = requests.get(url, auth=(cfg["username"], cfg["password"]))
    if r.status_code != 200:
        print("FAILED REQUEST")
        print("url:", r.url)
        print("status code:", r.status_code)
        print("headers\n", "-" * 70, sep="")
        print(r.headers)

    else:
        out = parse_response(r.text)
        print(out)


if __name__ == "__main__":
    main()
