from itertools import cycle
from manim import *
from manim import MathTex as MT
import icat_config  # to enable the I-Cat notation in all MathTex instances


def get_sub_indexes(tex):
    ni = VGroup()
    colors = cycle([RED,TEAL,GREEN,BLUE,PURPLE])
    for i in range(len(tex)):
        n = Text(f"{i}",color=next(colors)).scale(0.7)
        n.next_to(tex[i],DOWN,buff=0.01)
        ni.add(n)
    return ni


class Setup(Scene):
    """This scene just shows how the i-cat notation works."""

    def construct(self):
        # First example
        n1_1 = MT(r"0.1333...")
        n1_2 = MT(r"0.1333... = 0.1\overline{3}").move_to(n1_1.get_center())
        n1_3 = MT(r"0.1333... = 0.1\overline{3} = 0.1\icat^{\infty}3").move_to(n1_1.get_center())
        self.play(Write(n1_1))
        self.wait()
        self.play(TransformMatchingShapes(n1_1, n1_2), duration=2)
        self.wait()
        self.play(TransformMatchingShapes(n1_2, n1_3), duration=2)
        self.wait()
        
        # Second example
        n2_1 = MT(r"7.101010...")
        n2_2 = MT(r"7.101010... = 7.\overline{10}").move_to(n2_1.get_center())
        n2_3 = MT(r"7.101010... = 7.\overline{10} = 7.\icat^{\infty}10").move_to(n2_1.get_center())
        self.play(Write(n2_1), n1_3.animate.shift(UP))
        self.wait()
        self.play(TransformMatchingShapes(n2_1, n2_2), duration=2)
        self.wait()
        self.play(TransformMatchingShapes(n2_2, n2_3), duration=2)
        self.wait()

        # Third example
        n2_1 = MT(r"7.101010...")
        n2_2 = MT(r"7.101010... = 7.\overline{10}").move_to(n2_1.get_center())
        n2_3 = MT(r"7.101010... = 7.\overline{10} = 7.10\icat^{\infty}10").move_to(n2_1.get_center())
        self.play(Write(n2_1), n1_3.animate.shift(UP))
        self.wait()
        self.play(TransformMatchingShapes(n2_1, n2_2), duration=2)
        self.wait()
        self.play(TransformMatchingShapes(n2_2, n2_3), duration=2)
        self.wait()
        

class Simplest(Scene):
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


class Unpacking(Scene):
    def construct(self):
        pass


class Carrying(Scene):
    def construct(self):
        pass
