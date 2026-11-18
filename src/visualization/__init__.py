"""SanskritLens Visualization Package.

Provides Plotly and Matplotlib visualisations for token frequency,
length distributions, vocabulary composition, and Zipf rank analysis.
"""

from .charts import (
    plot_top_frequencies,
    plot_frequency_distribution,
    plot_word_length_distribution,
    plot_vocabulary_composition,
    plot_hapax_breakdown,
    plot_pareto_analysis,
    plot_frequency_rank_curve,
    generate_static_frequency_plot,
)

__all__ = [
    "plot_top_frequencies",
    "plot_frequency_distribution",
    "plot_word_length_distribution",
    "plot_vocabulary_composition",
    "plot_hapax_breakdown",
    "plot_pareto_analysis",
    "plot_frequency_rank_curve",
    "generate_static_frequency_plot",
]

