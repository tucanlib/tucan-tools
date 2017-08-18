# Tucan Grades Watcher

This (macOS) agent can be used to automatically check the grades for changes.

## Installation instructions
Note that this is macOS only - but it should be easily adaptable for other systems.

1) Adapt `$WORKDIR` and Python executable path in `tucan-grades`
2) Adapt paths in `de.david.tucan.agent.plist`. You can also change the interval controlling how often the grades should be crawled (in seconds).
3) Launch the agent: `launchctl load -w de.david.tucan.agent.plist`
