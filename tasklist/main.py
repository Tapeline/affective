from affective import handle, run
from affective.std.files import default_files_handler
from affective.std.stdio import default_stdio_handler
from tasklist.shell.storage.file_task_store import file_task_store_handler
from tasklist.shell.ui.console import run_console


if __name__ == "__main__":
    run(
        handle(
            run_console(),
            default_stdio_handler
            | default_files_handler
            | file_task_store_handler,
        )
    )
