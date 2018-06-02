import i3_memory_switcher
import unittest.mock as mock
import io


def test_saves_new_state(monkeypatch):
    """
    given we are are on workspace 1 and go to workspace 3, the space file should
    remember that the workspace before 3 was 1.
    """
    # patch the workspace lookup to simulate that we are on that workspace
    monkeypatch.setattr(
        i3_memory_switcher,
        'get_active_workspace_num',
        lambda: 1
    )
    # do not hit i3 during the test suite
    monkeypatch.setattr(
        i3_memory_switcher,
        'switch_to_workspace',
        lambda num: None
    )
    spaces = dict()
    # do the switch
    new_spaces = i3_memory_switcher.memory_switch(spaces, 3)
    assert new_spaces == {3: 1}


def test_returns_to_previous_space(monkeypatch):
    """
    given we are on workspace 3 and switch to 3, lookup the previous workspace
    and instead switch to that one
    """
    monkeypatch.setattr(
        i3_memory_switcher,
        'get_active_workspace_num',
        lambda: 3
    )
    # do not hit i3 during the test suite
    switch_to_workspace = mock.Mock()
    monkeypatch.setattr(
        i3_memory_switcher,
        'switch_to_workspace',
        switch_to_workspace
    )
    spaces = {3: 1}
    # do the switch
    new_spaces = i3_memory_switcher.memory_switch(spaces, 3)
    # the mocked switcher should have tried to go to 1 instead of 3
    switch_to_workspace.assert_called_with(1)
