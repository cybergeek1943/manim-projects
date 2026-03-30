r"""
Notes on LaTeX Environement:
eurosym is a LaTeX package that provides the Euro currency symbol (we use for I-Cat notation).
\mathop takes the \text{\euro} and treats it as an operator, which allows it to have limits (like ^2) placed above it with proper spacing.
The \limits command ensures that the superscript is placed directly above the symbol, rather than to the side, which is the default behavior for operators in LaTeX.
"""
from manim import *
from icat_mobject import *


# class IntegerMultiply(Scene):
#     def construct(self):
#         eq1 = MT(r"0.\overline{142857} = 0.\icat^{\infty}{(142857)}")
#         self.play(Write(eq1), run_time=2)
#         self.wait()

#         # second
#         eq2 = MT(r"0.\overline{142857} = 0.\icat^{\infty}{(142857)}").next_to(eq1, DOWN, buff=0.5)
#         self.play(TransformMatchingShapes(eq1.copy(), eq2), run_time=2)
#         self.wait()

#         # Draw the Plus sign and the Bar Line
#         plus_sign = MT(r"\times").next_to(eq2, LEFT, buff=0.5)
#         bar_line = Line(
#             plus_sign.get_left(), 
#             eq2.get_right()
#         ).next_to(eq2, DOWN, buff=0.5)
#         self.play(Write(plus_sign), Create(bar_line))
#         self.wait()


class AddNumbers_NoCarry(Scene):
    def construct(self):
        # Create numbers
        n1_1 = MT(r"0.3333\overline{3}").shift(LEFT * 2)
        n2_1 = MT(r"0.1666\overline{6}").shift(RIGHT * 2)
        self.play(Create(n1_1), Create(n2_1), run_time=1)
        self.wait()

        # Transform into I-Cat notation equations
        self.play(n1_1.animate.move_to(UP), n2_1.animate.move_to(DOWN))
        n1_2 = MT(r"0.3333\overline{3} = 0.\icat^{\infty}3").move_to(n1_1.get_center())
        n2_2 = MT(r"0.1666\overline{6} = 0.1\icat^{\infty}6").move_to(n2_1.get_center())
        self.play(
            TransformMatchingShapes(n1_1, n1_2), 
            TransformMatchingShapes(n2_1, n2_2), 
            run_time=2
        )
        self.wait()

        # Prepare for addition
        n1_3 = MT(r"0.3333\overline{3} = 0.3\icat^{\infty}3").move_to(n1_2.get_center())
        self.play(TransformMatchingShapes(n1_2, n1_3))
        self.wait()

        # Align for addition
        self.play(
            n2_2.animate.next_to(n1_3, DOWN, buff=0.4).align_to(n1_3, RIGHT)
        )

        # Draw the Plus sign and the Bar Line
        plus_sign = MT("+").next_to(n2_2, LEFT, buff=0.5)
        bar_line = Line(
            plus_sign.get_left(), 
            n2_2.get_right()
        ).next_to(n2_2, DOWN, buff=0.5)
        self.play(Write(plus_sign), Create(bar_line))
        self.wait()

        # Show the final added result below the line
        result = MT(r"0.4999\overline{9} = 0.4\icat^{\infty}9")
        result.next_to(bar_line, DOWN, buff=0.3).align_to(n2_2, RIGHT)
        
        self.play(TransformMatchingShapes(VGroup(n1_3, n2_2).copy(), result), run_time=3)
        self.wait(2)

        # Show the final result as 0.5
        final_result = MT(r"0.5 = 0.5\icat^{\infty}0").next_to(result, DOWN)
        self.play(TransformMatchingShapes(result.copy(), final_result), run_time=2)
        self.wait(2)
