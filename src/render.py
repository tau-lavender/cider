from src.singleton import Singleton

from textwrap import indent, dedent


class Render():
    def __init__(self):
        self.base_jenkins = dedent("""
                pipeline {{
                    agent any

                    stages {{
                {}
                    }}
                }}
            """).replace('\n', '', 1)

        self.base_stage = dedent("""
                stage('{}') {{
                    steps {{
                {}
                    }}
                }}
            """).replace('\n', '', 1)

    def render(self):
        singleton = Singleton()

        stages = []
        for stage_name in ("build", "test", "deploy"):
            stage = singleton.stages[stage_name]
            steps = []
            for job in stage.jobs:
                if job.runner == "sh":
                    steps.append(f"{job.runner} '{job.command}'")
                else:
                    steps.append(f"{job.runner} {job.command}")
            steps_render = "\n".join(steps)
            steps_render = indent(steps_render, " " * 4 * 2)

            stage_render = self.base_stage.format(
                stage.name,
                steps_render,
            )
            stages.append(stage_render)

        stages_render = "\n".join(stages)
        stages_render = indent(stages_render, " " * 4 * 2)

        result = self.base_jenkins.format(stages_render)
        return result
