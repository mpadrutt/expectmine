from curses import wrapper
from enum import Enum
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from pipeline.io.cli_io import CliIo
from pipeline.pipeline_new import Pipeline
from pipeline.storage.persistent_storage import PersistentStorage


class CLI(Enum):
    main_menu = 1
    build_pipeline = 2
    run_pipeline = 3
    exit_cli = 4


def build_pipeline(stdscr) -> tuple[CLI, Pipeline]:  # type: ignore
    pipeline_name = inquirer.text(message="Choose a name for your pipeline").execute()
    pipeline = Pipeline(pipeline_name)

    input_files: list[Path] = inquirer.checkbox(
        message="Select files",
        choices=[
            Choice(name=file.name, value=file)
            for file in Path("testdata").iterdir()
            if file.is_file()
        ],
    ).execute()

    pipeline.set_input_files(input_files)

    while True:
        if not (next_steps := pipeline.get_next_steps()):
            break

        if not (
            selected_step := inquirer.select(
                message="Select a step",
                choices=[Choice(name=step.name, value=step) for step in next_steps]
                + [Choice(name="Finish building pipeline", value=False)],
                multiselect=False,
            ).execute()
        ):
            break
        try:
            pipeline.add_step(selected_step, CliIo())
        except Exception as e:
            stdscr.addstr(str(e))
            stdscr.addstr("Press any key to continue")
            stdscr.getch()
            continue

    if inquirer.confirm(message="Do you want to save this pipeline?").execute():
        storage = PersistentStorage("Pipeline")

        pipelines = storage.get("pipelines")

        if not pipelines:
            pipelines: list[Pipeline] = []

        pipelines.append(pipeline)

        storage.store_object("pipelines", pipelines)

    if inquirer.confirm(message="Do you want to run this pipeline?").execute():
        return CLI.run_pipeline, pipeline
    else:
        return CLI.main_menu, pipeline


def run_pipeline(stdscr, pipeline: Pipeline | None = None) -> tuple[CLI, list[Path]]:
    if not pipeline:
        storage = PersistentStorage("Pipeline")
        if type(pipelines := storage.get("pipelines")) != list:
            stdscr.addstr("No pipelines found")
            stdscr.addstr("Press any key to continue")
            stdscr.getch()
            return CLI.main_menu, []

        if not (
            selected_pipeline := inquirer.select(
                message="Select a pipeline2",
                choices=[
                    Choice(name=str(p), value=p)  # type: ignore
                    for p in pipelines  # type: ignore
                ]
                + [Choice(name="Go back", value=None)],
                multiselect=False,
            ).execute()
        ):
            return CLI.main_menu, []

        input_files: list[Path] = inquirer.checkbox(
            message="Select input files",
            choices=[
                Choice(name=file.name, value=file)
                for file in Path("testdata").iterdir()
                if file.is_file()
                and file.suffix in selected_pipeline.get_input_filetypes()
            ],
        ).execute()

        selected_pipeline.set_input_files(input_files)
        pipeline: Pipeline = selected_pipeline

    try:
        output_path = inquirer.filepath(
            message="Select output folder",
            only_directories=True,
        ).execute()

        pipeline.set_output_path(Path(output_path).absolute())

        pipeline()
    except Exception as e:
        stdscr.addstr(str(e))
        stdscr.addstr("Press any key to continue")
        stdscr.getch()
        return CLI.main_menu, []

    return CLI.main_menu, []


def main_menu(stdscr):
    current_state: CLI = CLI.main_menu
    pipeline: Pipeline | None = None

    while True:
        stdscr.clear()
        stdscr.refresh()
        if current_state == CLI.main_menu:
            next_state = inquirer.select(
                message="Select files",
                choices=[
                    Choice(name="build pipeline", value=CLI.build_pipeline),
                    Choice(name="run pipeline", value=CLI.run_pipeline),
                    Choice(name="exit", value=CLI.exit_cli),
                ],
            ).execute()
            current_state = next_state

        elif current_state == CLI.build_pipeline:
            next_state, returned_pipeline = build_pipeline(stdscr)

            if next_state == CLI.run_pipeline and pipeline:
                pipeline = returned_pipeline

            current_state = next_state

        elif current_state == CLI.run_pipeline:
            next_state, filepaths = run_pipeline(stdscr, pipeline)

            current_state = next_state

        elif current_state == CLI.exit_cli:
            break


def run_cli():
    wrapper(main_menu)
