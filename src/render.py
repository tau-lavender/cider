from src.singleton import Singleton


class Render():
    def __init__(self):
        self.base_jenkins = """
                pipeline {
                    agent any

                    stages {
                        {}
                    }
                }
            """

        self.base_stage = """
                stage('{}') {
                    steps {
                        {}
                    }
                }
            """

    def render(self):
        singleton = Singleton()

        stages = []
        for stage in singleton.stages.values():
            steps = []
            for jobs in stage.jobs:
                steps.append(f"{jobs.runner} '{jobs.command}'")
            steps_render = "\n".join(steps)

            stage_render = self.base_stage.format(
                stage.name,
                steps_render,
            )
            stages.append(stage_render)

        stages_render = "\n".join(stages)

        result = self.base_jenkins.format(stages_render)
        return result
