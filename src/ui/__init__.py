"""SanskritLens User Interface Package.

Provides pages for Home, Input, Dashboard, Token Explorer, Insights,
Comparative Analysis, and Academic Methodology.
"""

from .home import render_home_page
from .input_page import render_input_page
from .dashboard import render_dashboard
from .token_explorer import render_token_explorer
from .insights import render_insights
from .comparative import render_comparative_page
from .methodology import render_methodology_page

__all__ = [
    "render_home_page",
    "render_input_page",
    "render_dashboard",
    "render_token_explorer",
    "render_insights",
    "render_comparative_page",
    "render_methodology_page",
]

