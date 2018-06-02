Say you're on workspace 3 and you want to go to workspace 4.

```
i3-memory-switch 4
```

Now you're on workspace 4 but you don't remember that you were on workspace 3 --
you just want to go back to the workspace you were on previously:

``
i3-memory-switch 4
```

The utility will notice that you asked it to send you to a workspace you are
already on -- so it'll go back to what it remembers was the workspace you were
just on. Now you're back on workspace 3.
