#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import subprocess
import sys

def add_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_image", required=True)
    parser.add_argument("--sandbox", required=True, help="sandbox path")
    parser.add_argument("--workspace", required=True, help="user workspace")
    parser.add_argument("--resolution", required=False, help="resolution: WxH")
    return parser


if __name__ == "__main__":
    args = add_parameter().parse_args()

    if os.path.exists(args.sandbox) and not os.path.isdir(args.sandbox):
        print "ERROR: Sandbox must be a directory."
        sys.exit(1)

    create_new_sandbox_requirement = [
        not os.path.exists(args.sandbox),
        os.path.exists(args.sandbox) and not os.listdir(args.sandbox)
    ]
    if any(create_new_sandbox_requirement):
        print "Create sandbox for image ..."
        ret_code = subprocess.call([
            "singularity", "build", "--sandbox", "-F",
            args.sandbox, args.base_image
        ])
        if ret_code != 0:
            sys.exit(1)
    
    cuda_devices = os.environ['CUDA_VISIBLE_DEVICES'].split(',')
    vnc_device = int(cuda_devices[0]) + 1
    display = ':' + str(vnc_device)
    vnc_port = str(5900 + vnc_device)
    no_vnc_port = str(6900 + vnc_device)
 
    print "Start Image ..."
    subprocess.call([
        "singularity", "exec", "--nv", "-w", "-B", args.workspace, args.sandbox, '/dockerstartup/vnc_startup_helper.sh',
        display, vnc_port, no_vnc_port, args.resolution
    ])

