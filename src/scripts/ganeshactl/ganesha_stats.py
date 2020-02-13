#!/usr/bin/python2
#
# This command receives statistics from Ganesha over DBus. The format
# for a command is:
#
# ganesha_stats <subcommand> <args>
#
# ganesha_stats help
#       To get detaled help
#
from __future__ import print_function
import sys
import time
import re
import Ganesha.glib_dbus_stats

def print_usage_exit(return_code):
    message = "\nUsage: \n"
    message += "Command displays global stats by default.\n"
    message += "\nTo display current status regarding stat counting use: \n"
    message += "  %s status \n" % (sys.argv[0])
    message += "\nTo display stat counters use: \n"
    message += "  %s [ list_clients | deleg <ip address> |\n" % (sys.argv[0])
    message += "          inode | iov3 [export id] | iov4 [export id] |\n"
    message += "          export | total [export id] | fast | pnfs [export id] |\n"
    message += "          fsal <fsal name> | v3_full | v4_full | auth |\n"
    message += "          client_io_ops <ip address> | export_details <export id> |\n"
    message += "          client_all_ops <ip address>] \n"
    message += "\nTo reset stat counters use: \n"
    message += "  %s reset \n" % (sys.argv[0])
    message += "\nTo enable/disable stat counters use: \n"
    message += "  %s [ enable | disable] [all | nfs | fsal | v3_full |\n" % (sys.argv[0])
    message += "           v4_full | auth | client_all_ops] \n"
    print(message)
    sys.exit(return_code)

if len(sys.argv) < 2:
    command = 'global'
else:
    command = sys.argv[1]

# check arguments
commands = ('help', 'list_clients', 'deleg', 'global', 'inode', 'iov3',
            'iov4', 'export', 'total', 'fast', 'pnfs', 'fsal', 'reset', 'enable',
            'disable', 'status', 'v3_full', 'v4_full', 'auth', 'client_io_ops',
            'export_details', 'client_all_ops')
if command not in commands:
    print("Option '%s' is not correct." % command)
    usage()
# requires an IP address
elif command in ('deleg'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by an ip address." % command)
        usage()
    command_arg = sys.argv[2]
# optionally accepts an export id
elif command in ('iov3', 'iov4', 'total', 'pnfs'):
    if (len(sys.argv) == 2):
        command_arg = -1
    elif (len(sys.argv) == 3) and sys.argv[2].isdigit():
        command_arg = sys.argv[2]
    else:
        usage()
elif command == "help":
    usage()
# requires fsal name
elif command in ('fsal'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by fsal name." % command)
        usage()
    command_arg = sys.argv[2]
elif command in ('enable', 'disable'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by all/nfs/fsal/v3_full/v4_full" %
            command)
        usage()
    command_arg = sys.argv[2]
    if command_arg not in ('all', 'nfs', 'fsal', 'v3_full', 'v4_full'):
        print("Option '%s' must be followed by all/nfs/fsal/v3_full/v4_full" %
            command)
        usage()

# retrieve and print stats
exp_interface = Ganesha.glib_dbus_stats.RetrieveExportStats()
cl_interface = Ganesha.glib_dbus_stats.RetrieveClientStats()
if command == "global":
    print(exp_interface.global_stats())
elif command == "export":
    print(exp_interface.export_stats())
elif command == "inode":
    print(exp_interface.inode_stats())
elif command == "fast":
    print(exp_interface.fast_stats())
elif command == "list_clients":
    print(cl_interface.list_clients())
elif command == "deleg":
    print(cl_interface.deleg_stats(command_arg))
elif command == "iov3":
    print(exp_interface.v3io_stats(command_arg))
elif command == "iov4":
    print(exp_interface.v4io_stats(command_arg))
elif command == "total":
    print(exp_interface.total_stats(command_arg))
elif command == "pnfs":
    print(exp_interface.pnfs_stats(command_arg))
elif command == "reset":
    print(exp_interface.reset_stats())
elif command == "fsal":
    print(exp_interface.fsal_stats(command_arg))
elif command == "v3_full":
    print(exp_interface.v3_full_stats())
elif command == "v4_full":
    print(exp_interface.v4_full_stats())
elif command == "enable":
    print(exp_interface.enable_stats(command_arg))
elif command == "disable":
    print(exp_interface.disable_stats(command_arg))
elif command == "status":
    print(exp_interface.status_stats())
