import os
import subprocess
from typing import Any, Optional
from lib import PluginStep, Config
from typing_extensions import TypedDict
from jinja2 import FileSystemLoader, select_autoescape, Environment


class FileGenerationOptions(TypedDict, total=False):
    template_directory: str
    template_name: str
    output_path: str
    variables: dict[str, Any]
    escape_extensions: Optional[list[str]]


class GenerateFile(PluginStep[FileGenerationOptions]):
    def __init__(self, config: Config, directory: str, options: FileGenerationOptions):
        super().__init__(config, directory, options)
        self.env = Environment(
            loader=FileSystemLoader(self.options["template_directory"]),
            autoescape=(
                select_autoescape(
                    enabled_extensions=self.options["escape_extensions"])
                if self.options.get("escape_extensions")
                else False
            ),
        )

    def execute(self):
        template = self.env.get_template(self.options["template_name"])
        with open(os.path.join(self.directory, self.options["output_path"]), "w") as f:
            f.write(template.render(self.options["variables"]))


class ScriptExecutionOptions(TypedDict, total=False):
    command: str
    args: list[str]


class ExecuteScript(PluginStep[ScriptExecutionOptions]):
    def execute(self):
        subprocess.check_call(
            [self.options["command"], *self.options.get("args", [])], cwd=self.directory)


BASE_STEPS = {
    "file_generation": GenerateFile,
    "exec_script": ExecuteScript
}
