# Python Pomodoro

A simple pomodoro timer application used in the command line written in Python.

I chose to do this project in order to learn more about command line interface tooling. I find CLIs fascinating and wanted to understand what is happening behind the scenes.

<!--
Used `uv` to manage dependencies and the virtual environment.
Created the project using `uv init --package python_pomodoro`
The `--package`` flag creates a `src` and a module directory, an `__init__.py` in the module directory, adds a build system, and creates a command(?).

Things to write about:
- Contemplated CLI vs TUI
- config schema organization and validation
- nohup and & vs daemon
- race conditions (atomic writes vs file locking)
- the project blew up into something way more complex than I thought it would be. (Scope creep?)
- maybe I should have started with the timer and worked on the config later. I'm not sure yet if there is a right and wrong way (config/state management first / business logic first / work on them together in feature based development?)

Future goals:
- handle race conditions (atomic writes vs file locking)
- implement daemon (with automatic restart and logging/error handling)
-->
