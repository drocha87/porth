#!/usr/bin/env python3

import sys
import os
import subprocess
import shlex

def cmd_run_echoed(cmd, **kwargs):
    print("[CMD] %s" % " ".join(map(shlex.quote, cmd)))
    cmd = subprocess.run(cmd, **kwargs)
    if cmd.returncode != 0:
        print(cmd.stdout.decode('utf-8'), file=sys.stdout)
        print(cmd.stderr.decode('utf-8'), file=sys.stderr)
        exit(cmd.returncode)
    return cmd

def test(folder):
    com_failed = 0
    for entry in os.scandir(folder):
        porth_ext = '.porth'
        if entry.is_file() and entry.path.endswith(porth_ext):
            print('[INFO] Testing %s' % entry.path)

            txt_path = entry.path[:-len(porth_ext)] + ".txt"
            expected_output = None
            with open(txt_path, "rb") as f:
                expected_output = f.read()

            com_output = cmd_run_echoed(["./porth.py", "com", "-r", "-s", entry.path], capture_output=True).stdout
            if com_output != expected_output:
                com_failed += 1
                print("[ERROR] Unexpected compilation output")
                print("  Expected:")
                print("    %s" % expected_output)
                print("  Actual:")
                print("    %s" % com_output)
                # exit(1)
    print()
    print("Test failed: %d" % (com_failed))
    if com_failed != 0:
        exit(1)

def record(folder):
    for entry in os.scandir(folder):
        porth_ext = '.porth'
        if entry.is_file() and entry.path.endswith(porth_ext):
            output = cmd_run_echoed(["./porth.py", "com", "-r", "-s", entry.path], capture_output=True).stdout
            txt_path = entry.path[:-len(porth_ext)] + ".txt"
            print("[INFO] Saving output to %s" % txt_path)
            with open(txt_path, "wb") as txt_file:
                txt_file.write(output)

def usage(exe_name):
    print("Usage: ./test.py [OPTIONS] [SUBCOMMAND]")
    print("OPTIONS:")
    print("    -f <folder>   Folder with the tests. (Default: ./tests/)")
    print("SUBCOMMANDS:")
    print("    test          Run the tests. (Default when no subcommand is provided)")
    print("    record        Record expected output of the tests.")
    print("    help          Print this message to stdout and exit with 0 code.")

# TODO: test compiler errors

if __name__ == '__main__':
    exe_name, *argv = sys.argv

    folder = "./tests/"
    subcmd = "test"

    while len(argv) > 0:
        arg, *argv = argv
        if arg == '-f':
            if len(argv) == 0:
                print("[ERROR] no <folder> is provided for option `-f`")
                exit(1)
            folder, *argv = argv
        else:
            subcmd = arg
            break

    if subcmd == 'record':
        record(folder)
    elif subcmd == 'test':
        test(folder)
    elif subcmd == 'help':
        usage(exe_name)
    else:
        usage(exe_name)
        print("[ERROR] unknown subcommand `%s`" % subcmd, file=sys.stderr)
        exit(1);
