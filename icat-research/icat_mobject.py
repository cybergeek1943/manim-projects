from manim import *
template = TexTemplate()
template.add_to_preamble(r"\usepackage{eurosym}")
template.add_to_preamble(r"\newcommand{\icat}{\mathop{\text{\euro}}\limits}")


class MT(MathTex):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, tex_template=template)
