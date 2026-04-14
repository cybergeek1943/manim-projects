r"""
Notes on LaTeX Environement:
eurosym is a LaTeX package that provides the Euro currency symbol (we use for I-Cat notation).
\mathop takes the \text{\euro} and treats it as an operator, which allows it to have limits (like ^2) placed above it with proper spacing.
The \limits command ensures that the superscript is placed directly above the symbol, rather than to the side, which is the default behavior for operators in LaTeX.
"""
from manim import TexTemplate, config
template = TexTemplate()
template.add_to_preamble(r"\usepackage{eurosym}")
template.add_to_preamble(r"\newcommand{\icat}{\mathop{\text{\euro}}\limits}")
config.tex_template = template

# we could also subclass if we want to add more functionality, but for now using config is sufficient
# from typing import TYPE_CHECKING
# class MathTex(_MathTex):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs, tex_template=template)
# if TYPE_CHECKING:
#     class MathTex(_MathTex):
#         pass
