#!/usr/bin/env python3
import subprocess
import json
import sys
import os


def get_active_workspace_num():
    results = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
    results.check_returncode()
    spaces = json.loads(results.stdout)
    active = [i for i in spaces if i['focused']]
    return active[0]['num']


def switch_to_workspace(num):
    cmd = 'workspace {}'.format(num)
    results = subprocess.run(['i3-msg', '-t', 'command', cmd], stdout=subprocess.PIPE)

def memory_switch(spaces, num):
    current = get_active_workspace_num()
    if num == current:
        # you are doing the switchback
        next_space = spaces.get(num)
        if next_space:
            switch_to_workspace(next_space)
    else:
        # you are doing a regular switch and should record things

        # this is going to mutate the dictionary, which i feel gross about
        # but it's probably overkill to remain immutable
        spaces[num] = current
        switch_to_workspace(num)
    return spaces


def parse_spaces(s):
    """
    the format of a space file is going to be a jank almost csv
    that just has two columns of integers:

    1,2
    2,4
    
    if it ever gets more complicated than that, use a csv lib
    """
    o = dict()
    for line in s.split():
        k, v = line.strip().split(',')
        o[int(k)] = int(v)
    return o

def format_spaces(spaces):
    pairs = [str(k) + ',' + str(v) for k, v in spaces.items()]
    return '\n'.join(pairs)

def get_space_file_path():
    """
    i would ultimately want this to be some kind of kv store that only lives
    during the user's i3 session, but i don't know how to do that.

    instead i'll try to make it a file that sits next to wherever the user has
    installed the script.  i wasn't sure if that is better than putting it in a
    fixed location on all computers or in the user's homedir
    """
    d = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.join(d, 'space_file')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        prog_name = sys.argv[0]
        print('usage: {} NUMBER'.format(prog_name))
        sys.exit(1)

    workspace_num = int(sys.argv[1])
    space_file = get_space_file_path()
    with open(space_file, 'a+') as sp:
        sp.seek(0)
        spaces = parse_spaces(sp.read())
        # do switch stuff
        spaces = memory_switch(spaces, workspace_num)
        # save
        # i am probably doing something wrong with files. this feels ugly
        sp.seek(0)
        sp.truncate()
        o = format_spaces(spaces)
        sp.write(o)
