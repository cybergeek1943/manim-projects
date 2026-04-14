from itertools import cycle
from manim import *
from manim import MathTex as MT
import config  # to enable the I-Cat notation in all MathTex instances


def get_sub_indexes(tex):
    ni = VGroup()
    colors = cycle([RED,TEAL,GREEN,BLUE,PURPLE])
    for i in range(len(tex)):
        n = Text(f"{i}",color=next(colors)).scale(0.7)
        n.next_to(tex[i],DOWN,buff=0.01)
        ni.add(n)
    return ni


class Setup(Scene):
    """This scene just shows how the i-cat notation works.
    
    TODO:
    - show more cases of the index being used for non-infinite repeats.
    """
    def construct(self):
            self.add(Text("I-Cat Notation Example", font_size=36).to_corner(UL, 0.5))

            def animate_icat_conversion(step1_str, step2_str, step3_str, move_to_init: Vector = None, move_to_after: Vector = None):
                eq1 = MT(step1_str)
                eq2 = MT(step1_str, step2_str)
                eq3 = MT(step1_str, step2_str, step3_str)
                if move_to_init is not None:
                    eq1.move_to(move_to_init)
                self.play(Write(eq1))
                self.wait(0.5)
                eq2.move_to(eq1) 
                self.play(TransformMatchingTex(eq1, eq2), run_time=2)
                self.wait(0.5)
                eq3.move_to(eq2)
                self.play(TransformMatchingTex(eq2, eq3), run_time=2)
                self.wait(0.5)
                if move_to_after is not None:
                    self.play(eq3.animate.move_to(move_to_after))

            animate_icat_conversion(
                r"0.1333...", 
                r" = 0.1\overline{3}",
                r" = 0.1\icat^{\infty}3",
                move_to_after=UP
            )

            self.play(Write(Text('and', font_size=24)))
            
            animate_icat_conversion(
                r"7.101010...", 
                r" = 7.\overline{10}", 
                r" = 7.\icat^{\infty}(10)",
                move_to_init=DOWN
            )

            self.wait(4)


class Simplest(Scene):
    def construct(self):
        title = Text("Simple Addition", font_size=36).to_corner(UL, 0.5)
        self.add(title)

        # Create numbers
        n1 = MT(r"0.78282828282828282").shift(UP)
        n2 = MT(r"0.21313131313131313").shift(DOWN)
        self.play(Create(n1), Create(n2), run_time=1)
        self.wait()

        # show notes
        note = Text('We want to add these.', font_size=20);
        self.play(Create(note))
        self.wait()
        self.play(Transform(note, Text("Let's look at the I-Cat form.", font_size=20)))
        self.wait()

        # transform to i-cat
        n1t = MT(r'0.7 \icat^9 (82)').move_to(n1)
        n2t = MT(r'0.2 \icat^9 (13)').move_to(n2)
        self.play(TransformMatchingShapes(n1, n1t), run_time=2)
        self.play(TransformMatchingShapes(n2, n2t), run_time=2)
        n1, n2 = n1t, n2t
        self.wait()

        # move to adding line
        addition_stack = VGroup(n1, n2)
        self.play(
            addition_stack.animate.arrange(DOWN, buff=0.3, aligned_edge=RIGHT),
            FadeOut(note)
        )
        plus_sign = MT('+').next_to(n2, LEFT, buff=0.5)
        line = Line().scale_to_fit_width(addition_stack.width + 1.2).next_to(addition_stack, DOWN, buff=0.5)
        addition_group = VGroup(addition_stack, plus_sign, line)
        self.play(
            FadeIn(line),
            FadeIn(plus_sign),
            run_time=0.5
        )
        self.play(addition_group.animate.shift(RIGHT))
        note.become(Text('Pre-check:\n• Aligned?\n• Index?', font_size=25, line_spacing=1.5)).to_edge(buff=2)
        self.play(FadeIn(note))
        self.wait()

        # alignment check
        box = SurroundingRectangle(VGroup(n1[0][0], n2[0][0]), color=YELLOW, buff=0.1)
        self.play(Create(box))
        for i in (2, slice(3, 5), slice(3, 7), slice(3, 9)):
            target_box = SurroundingRectangle(VGroup(n1[0][i], n2[0][i]), color=GREEN if i == slice(3, 9) else YELLOW, buff=0.1)
            self.play(
                Transform(box, target_box)
            )
            self.wait(0.2)
        self.play(  # transform surround box into label
            ReplacementTransform(box, note[10:18]),
            note[10:18].animate.set_color(GREEN),
            note[18].animate.set_color(BLACK),  # hide the question mark
        )
        self.wait()

        # index check
        self.play(
            n1[0][3].animate.set_color(ORANGE).scale(2),
            n2[0][3].animate.set_color(ORANGE).scale(2),
            rate_func=there_and_back,
        )
        index_eq = MT('9 = 9').next_to(note[25], buff=0.8)
        self.play(ReplacementTransform(VGroup(n1[0][3].copy(), n2[0][3].copy()), index_eq))
        self.play(index_eq.animate.set_color(GREEN))
        self.wait()
        self.play(  # transform index_eq into label
            ReplacementTransform(index_eq, note[19:25]),
            note[19:25].animate.set_color(GREEN),
            note[25].animate.set_color(BLACK),  # hide the question mark
        )

        # center the addition_group
        self.play(
            FadeOut(note),
            addition_group.animate.center()
        )
        self.wait()

        # calculate sum
        box = SurroundingRectangle(VGroup(n1[0][7:9], n2[0][7:9]), color=BLUE, buff=0.1)
        self.play(Create(box))
        final_sum = MT(r"0.9 \icat^9 (95)").next_to(line, DOWN, buff=0.3)
        final_sum.align_to(addition_stack, RIGHT) # Align the whole block to the stack
        final_sum.set_opacity(0) # Hide it initially
        self.add(final_sum)
        for i in (slice(7, 9), 6, slice(3, 6), 2, slice(0, 2)):            
            # Move the highlight box
            target_box = SurroundingRectangle(VGroup(n1[0][i], n2[0][i]), color=BLUE, buff=0.1)
            self.play(Transform(box, target_box))
            
            # The Merge Animation
            # We transform the numbers into the specific, pre-aligned part of final_sum
            self.play(
                ReplacementTransform(n1[0][i].copy(), final_sum[0][i]),
                ReplacementTransform(n2[0][i].copy(), final_sum[0][i]),
                final_sum[0][i].animate.set_opacity(1), # Reveal only this digit
            )
            self.wait(0.2)
        target_box = SurroundingRectangle(final_sum, addition_group, color=GREEN, buff=0.2)
        self.play(ReplacementTransform(box, target_box))
        
        # final answer
        final_group = VGroup(final_sum, addition_group, target_box)
        self.play(
            final_group.animate.center()
        )
        self.play(
            final_group.animate.scale(1.4),
            Uncreate(target_box)
        )
        self.wait(4)


class Unpacking(Scene):
    def construct(self):
        title = Text("Addition: Alignment Unpacking", font_size=36).to_corner(UL, 0.5)
        self.add(title)

        # Create numbers
        n1 = MT(r'0.2 \icat^5 4').shift(UP)
        n2 = MT(r'0.3 \icat^6 5').shift(DOWN)
        self.play(Create(n1), Create(n2), run_time=1)
        self.wait()

        # show notes
        note = Text('We want to add these two I-Cats.', font_size=20);
        self.play(Create(note))
        self.wait()

        # move to adding line
        addition_stack = VGroup(n1, n2)
        self.play(
            addition_stack.animate.arrange(DOWN, buff=0.3, aligned_edge=RIGHT),
            FadeOut(note)
        )
        plus_sign = MT('+').next_to(n2, LEFT, buff=0.5)
        line = Line().scale_to_fit_width(addition_stack.width + 1.2).next_to(addition_stack, DOWN, buff=0.5)
        addition_group = VGroup(addition_stack, plus_sign, line)
        self.play(
            FadeIn(line),
            FadeIn(plus_sign),
            run_time=0.5
        )

        # index check
        self.play(
            n1[0][3].animate.set_color(ORANGE).scale(2),
            n2[0][3].animate.set_color(ORANGE).scale(2),
            rate_func=there_and_back,
        )
        index_eq = MT(r'{{5}} \neq 6').next_to(n1[0][3], UP, buff=0.8)
        self.play(ReplacementTransform(VGroup(n1[0][3].copy(), n2[0][3].copy()), index_eq))
        self.play(index_eq.animate.set_color(RED))
        self.wait()

        # partially unpack
        n1t = MT(r'0.2 \icat^5 (4) 0').move_to(n1)
        n2t = MT(r'0.3 \icat^5 (5) 5').move_to(n2)
        index_eq_t = MT(r'{{5}} = 5').next_to(n1t[0][3], UP, buff=0.8).set_color(GREEN)
        self.play(
            TransformMatchingShapes(n2, n2t),
            TransformMatchingShapes(n1, n1t),
            TransformMatchingTex(index_eq, index_eq_t, transform_mismatches=True),
            run_time = 4
        )
        n1, n2, index_eq = n1t, n2t, index_eq_t
        addition_stack.submobjects = [n1, n2]
        self.wait()

        # center the addition_group
        self.play(
            FadeOut(index_eq_t),
            addition_group.animate.center()
        )
        self.wait()

        # calculate sum
        box = SurroundingRectangle(VGroup(n1[0][8], n2[0][8]), color=BLUE, buff=0.1)
        self.play(Create(box))
        final_sum = MT(r"0.5 \icat^5 (9) 5").next_to(line, DOWN, buff=0.3)
        final_sum.align_to(addition_stack, RIGHT) # Align the whole block to the stack
        final_sum.set_opacity(0) # Hide it initially
        self.add(final_sum)
        for i in (8, slice(3, 8), 2, slice(0, 2)):            
            # Move the highlight box
            target_box = SurroundingRectangle(VGroup(n1[0][i], n2[0][i]), color=BLUE, buff=0.1)
            self.play(Transform(box, target_box))
            
            # The Merge Animation
            # We transform the numbers into the specific, pre-aligned part of final_sum
            self.play(
                ReplacementTransform(n1[0][i].copy(), final_sum[0][i]),
                ReplacementTransform(n2[0][i].copy(), final_sum[0][i]),
                final_sum[0][i].animate.set_opacity(1), # Reveal only this digit
            )
            self.wait(0.2)
        target_box = SurroundingRectangle(final_sum, addition_group, color=GREEN, buff=0.2)
        self.play(ReplacementTransform(box, target_box))
        
        # final answer
        final_group = VGroup(final_sum, addition_group, target_box)
        self.play(
            final_group.animate.center()
        )
        self.play(
            final_group.animate.scale(1.3),
            Uncreate(target_box)
        )
        self.wait(4)



class Carrying(Scene):
    def construct(self):
        pass
