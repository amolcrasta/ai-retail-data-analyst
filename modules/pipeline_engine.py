class PipelineEngine:

    def __init__(self, modules):

        self.modules = modules

    def run(self, context):

        for module in self.modules:

            context = module.run(context)

        return context