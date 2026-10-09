"""Project-wide settings for the churn model."""

# The column the model learns to predict: 1 if the customer left, else 0.
LABEL_COLUMN = "churned"

# The input columns the model is allowed to learn from.
FEATURE_COLUMNS = ("tenure_months", "monthly_charges", "support_tickets")

# Fixed seed for every random step, so the same data always gives the
# same split and the same results.
RANDOM_SEED = 42

# Share of rows held out for evaluation.
TEST_FRACTION = 0.2
