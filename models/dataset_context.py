class DatasetContext:

    def __init__(self):

        self.datasets = []
        self.dataset_names = []

        self.cleaned_dataframe = None

        self.detected_relationships = []
        self.joins = []

        self.visualizations = []

        # AI pipeline logging
        self.transformation_history = []

        # optional AI insights
        self.ai_insights = []
