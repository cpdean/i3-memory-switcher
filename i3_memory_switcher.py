import subprocess
import json


def get_active_workspace_num():
    results = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
    results.check_returncode()
    spaces = json.loads(results.stdout)
    active = [i for i in spaces if i['focused']]
    return active[0]['num']


def switch_to_workspace(num):
    cmd = '"workspace {}"'.format(num)
    results = subprocess.run(['i3-msg', '-t', 'command', cmd], stdout=subprocess.PIPE)

def memory_switch(spaces, num):
    current = get_active_workspace_num()
    if num == current:
        # you are doing the switchback
        next_space = spaces.get(num)
        if next_space:
            switch_to_workspace(num)
    else:
        # you are doing a regular switch and should record things

        # this is going to mutate the dictionary, which i feel gross about
        # but it's probably overkill to remain immutable
        spaces[current] = num
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
    print('here are the file contents')
    print(' "{}" '.format(s))
    for line in s.split():
        k, v = line.strip().split(',')
        o[int(k)] = int(v)
    return o

def format_spaces(spaces):
    pairs = [str(k) + ',' + str(v) for k, v in spaces.items()]
    return '\n'.join(pairs)


if __name__ == '__main__':
    with open('space_file', 'a+') as sp:
        sp.seek(0)
        spaces = parse_spaces(sp.read())
        print('old values')
        print(spaces)
        # do switch stuff
        spaces = {2: 3}
        # save
        # i am probably doing something wrong with files. this feels ugly
        sp.seek(0)
        sp.truncate()
        o = format_spaces(spaces)
        print('going to write "{}"'.format(o))
        sp.write(o)
