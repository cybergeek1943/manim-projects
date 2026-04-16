from manim import *
from manim import MathTex as MT
import config  # to enable the I-Cat notation in all MathTex instances


def animate_sum_steps(self: Scene, n1: MT, n2: MT, final_sum: MT, box: SurroundingRectangle, slices: list[int | slice | tuple[int | slice, ...]], t_slice_map: dict[int | slice, int | slice] = None):
    if t_slice_map is None:
        t_slice_map = {}
    for i in slices:  
        if isinstance(i, tuple):
            n1_src = VGroup(*[n1[0][j] for j in i])
            n2_src = VGroup(*[n2[0][j] for j in i])
            target = VGroup(*[final_sum[0][t_slice_map.get(j, j)] for j in i])
            i = i[0]  # because the target_box uses i
        else:
            n1_src = n1[0][i]
            n2_src = n2[0][i]
            target = final_sum[0][t_slice_map.get(i, i)]
        target_box = SurroundingRectangle(VGroup(n1[0][i], n2[0][i]), color=BLUE, buff=0.1)
        self.play(Transform(box, target_box))
        self.play(
            ReplacementTransform(n1_src.copy(), target),
            ReplacementTransform(n2_src.copy(), target),
            target.animate.set_opacity(1), # Reveal only this digit
        )
        self.wait(0.2)


class Setup(Scene):
    """This scene just shows how the i-cat notation works."""
    def construct(self):
            self.add(Text("I-Cat Notation Example", font_size=36).to_corner(UL, 0.5))

            def animate_icat_conversion(
                    step1_str,
                    step2_str,
                    step3_str,
                    init_move_to: Vector = None
                ) -> MT:
                eq1 = MT(step1_str)
                if init_move_to is not None:
                    eq1.move_to(init_move_to)
                if step2_str:
                    eq2 = MT(step1_str, step2_str)
                if step3_str:
                    eq3 = MT(step1_str, step2_str, step3_str)

                self.play(Write(eq1))
                self.wait(0.5)
                if not step2_str:
                    return eq1

                eq2.move_to(eq1)
                self.play(TransformMatchingTex(eq1, eq2), run_time=2)
                self.wait(0.5)
                if not step3_str:
                    return eq2

                eq3.move_to(eq2)
                self.play(TransformMatchingTex(eq2, eq3), run_time=2)
                self.wait(0.5)
                return eq3
            
            a1 = animate_icat_conversion(
                r"0.1333...", 
                r" = 0.1\overline{3}",
                r" = 0.1\icat^{\infty}3",
            )

            and_text = Text('or', font_size=24)
            self.play(
                a1.animate.shift(UP),
                FadeIn(and_text)
            )
            
            a2 = animate_icat_conversion(
                r"7.101010...", 
                r" = 7.\overline{10}", 
                r" = 7.\icat^{\infty}(10)",
                init_move_to=DOWN
            )

            self.play(
                and_text.animate.shift(DOWN),
                a2.animate.shift(UP)
            )

            a3 = animate_icat_conversion(
                r"205555555456456456", 
                r" = 20 \icat^5 5 \icat^3 (456)", 
                "",
                init_move_to=DOWN * 2
            )

            self.play(
                FadeOut(and_text),
                a3.animate.move_to(DOWN)
            )

            self.wait(5)


class Simplest_V1(Scene):
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
        note.become(Text('Pre-check:\n• Aligned?\n• Index?', font_size=25, line_spacing=1.5)).to_edge(buff=2)
        self.play(FadeIn(note), addition_group.animate.shift(RIGHT))
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
            Indicate(n1[0][3], scale_factor=2, color=ORANGE),
            Indicate(n2[0][3], scale_factor=2, color=ORANGE)
        )
        index_eq = MT('9 = 9').next_to(note[25], buff=0.8)
        self.play(ReplacementTransform(VGroup(n1[0][3].copy(), n2[0][3].copy()), index_eq))
        self.play(index_eq.animate.set_color(GREEN))
        self.wait(0.4)
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
        box = SurroundingRectangle(VGroup(n1[0][7], n2[0][7]), color=BLUE, buff=0.1)
        self.play(Create(box))
        final_sum = MT(r"0.9 \icat^9 (95)").next_to(line, DOWN, buff=0.3)
        final_sum.align_to(addition_stack, RIGHT) # Align the whole block to the stack
        final_sum.set_opacity(0) # Hide it initially
        self.add(final_sum)
        animate_sum_steps(self, n1, n2, final_sum, box, [7, 6, (slice(3, 5), 5, 8), 2, (0, 1)])
        target_box = SurroundingRectangle(final_sum, addition_group, color=GREEN, buff=0.2)
        self.play(ReplacementTransform(box, target_box))
        
        # final answer
        final_group = VGroup(final_sum, addition_group, target_box)
        self.play(
            final_group.animate.center()
        )
        self.play(
            final_group.animate.scale(1.2),
            Uncreate(target_box)
        )
        self.wait(5)


class Simplest_V2(Scene):
    def construct(self):
        title = Text("Simple Addition", font_size=36).to_corner(UL, 0.5)
        self.add(title)

        # Create numbers
        n1 = MT(r"0.78888888882").shift(UP)
        n2 = MT(r"0.21111111113").shift(DOWN)
        self.play(Create(n1), Create(n2), run_time=1)
        self.wait()

        # show notes
        note = Text('We want to add these.', font_size=20);
        self.play(Create(note))
        self.wait()
        self.play(Transform(note, Text("Let's look at the I-Cat form.", font_size=20)))
        self.wait()

        # transform to i-cat
        n1t = MT(r'0.7 \icat^9 (8) 2').move_to(n1)
        n2t = MT(r'0.2 \icat^9 (1) 3').move_to(n2)
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
        note.become(Text('Pre-check:\n• Aligned?\n• Index?', font_size=25, line_spacing=1.5)).to_edge(buff=2)
        self.play(FadeIn(note), addition_group.animate.shift(RIGHT))
        self.wait()

        # alignment check
        box = SurroundingRectangle(VGroup(n1[0][0], n2[0][0]), color=YELLOW, buff=0.1)
        self.play(Create(box))
        for i in (2, slice(3, 5), slice(3, 8)):
            target_box = SurroundingRectangle(VGroup(n1[0][i], n2[0][i]), color=GREEN if i == slice(3, 8) else YELLOW, buff=0.1)
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
            Indicate(n1[0][3], scale_factor=2, color=ORANGE),
            Indicate(n2[0][3], scale_factor=2, color=ORANGE)
        )
        index_eq = MT('9 = 9').next_to(note[25], buff=0.8)
        self.play(ReplacementTransform(VGroup(n1[0][3].copy(), n2[0][3].copy()), index_eq))
        self.play(index_eq.animate.set_color(GREEN))
        self.wait(0.4)
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
        box = SurroundingRectangle(VGroup(n1[0][8], n2[0][8]), color=BLUE, buff=0.1)
        self.play(Create(box))
        final_sum = MT(r"0.9 \icat^9 (9) 5").next_to(line, DOWN, buff=0.3)
        final_sum.align_to(addition_stack, RIGHT) # Align the whole block to the stack
        final_sum.set_opacity(0) # Hide it initially
        self.add(final_sum)
        animate_sum_steps(self, n1, n2, final_sum, box, [8, 6, (slice(3, 5), 5, 7), 2, (0, 1)])
        target_box = SurroundingRectangle(final_sum, addition_group, color=GREEN, buff=0.2)
        self.play(ReplacementTransform(box, target_box))
        
        # final answer
        final_group = VGroup(final_sum, addition_group, target_box)
        self.play(
            final_group.animate.center()
        )
        self.play(
            final_group.animate.scale(1.2),
            Uncreate(target_box)
        )
        self.wait(5)


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
        note = Text('We want to add these.', font_size=20);
        self.play(Create(note))
        self.wait()

        # move to adding line
        addition_stack = VGroup(n1, n2)
        self.play(
            addition_stack.animate.arrange(DOWN, buff=0.3, aligned_edge=LEFT),
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
            Indicate(n1[0][3], scale_factor=2, color=ORANGE),
            Indicate(n2[0][3], scale_factor=2, color=ORANGE)
        )
        index_eq = MT(r'{{5}} \neq 6').next_to(n1[0][3], UP, buff=0.8)
        self.play(ReplacementTransform(VGroup(n1[0][3].copy(), n2[0][3].copy()), index_eq))
        self.play(index_eq.animate.set_color(RED))
        self.wait()

        # partially unpack
        n1t = MT(r'0.2 \icat^5 (4) 0').move_to(n1, LEFT)
        n2t = MT(r'0.3 \icat^5 (5) 5').move_to(n2, LEFT)
        index_eq_t = MT(r'{{5}} = 5').next_to(n1t[0][3], UP, buff=0.8).set_color(GREEN)
        self.play(
            TransformMatchingShapes(n2, n2t),
            TransformMatchingTex(index_eq, index_eq_t, transform_mismatches=True),
            run_time = 4
        )
        self.play(TransformMatchingShapes(n1, n1t))
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
        final_sum.align_to(addition_stack, RIGHT)  # Align the whole block to the stack
        final_sum.set_opacity(0)  # Hide it initially
        self.add(final_sum)
        animate_sum_steps(self, n1, n2, final_sum, box, [8, 6, (slice(3, 5), 5, 7), 2, (0, 1)])
        target_box = SurroundingRectangle(final_sum, addition_group, color=GREEN, buff=0.2)
        self.play(ReplacementTransform(box, target_box))
        
        # final answer
        final_group = VGroup(final_sum, addition_group, target_box)
        self.play(
            final_group.animate.center()
        )
        self.play(
            final_group.animate.scale(1.2),
            Uncreate(target_box)
        )
        self.wait(4)


class Carrying(MovingCameraScene):
    def construct(self):
        title = Text("Addition: Carrying", font_size=36).to_corner(UL, 0.5)
        self.add(title)

        # Create numbers
        n1 = MT('1.45').shift(UP)
        n2 = MT(r'1. \icat^5 6').shift(DOWN)
        self.play(Create(n1), Create(n2), run_time=1)
        self.wait()

        # show notes
        note = Text('We want to add these.', font_size=20);
        self.play(Create(note))
        self.wait()

        # move to adding line
        addition_stack = VGroup(n1, n2)
        self.play(
            addition_stack.animate.arrange(DOWN, buff=0.3, aligned_edge=LEFT),
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

        # alignment check
        box = SurroundingRectangle(VGroup(n1[0][2:], n2[0][2:]), color=RED, buff=0.1)
        self.play(Create(box))
        note.become(Text('Misaligned!', font_size=25, color=RED)).next_to(addition_group, UP, buff=0.8)
        self.play(ReplacementTransform(box, note))
        self.wait()
        self.play(Transform(note, Text('Prepare: Partially Unpack', font_size=25, color=GREEN).move_to(note)))
        self.wait()

        # partially unpack
        n2t1 = MT(r'1.6 \icat^4 6').move_to(n2, LEFT)
        self.play(TransformMatchingShapes(n2, n2t1))
        n2t2 = MT(r'1.66 \icat^3 6').move_to(n2, LEFT)
        self.play(TransformMatchingShapes(n2t1, n2t2))
        n1t = MT(r'1.45 \icat^3 0').move_to(n1, LEFT+DOWN)
        self.play(TransformMatchingShapes(n1, n1t))
        n1, n2 = n1t, n2t2
        addition_stack.submobjects = [n1, n2]
        self.wait()

        # center the addition_group
        self.play(
            FadeOut(note),
            addition_group.animate.center()
        )

        # calculate initial sum (with carry pre-superscripts)
        box = SurroundingRectangle(VGroup(n1[0][6], n2[0][6]), color=BLUE, buff=0.1)
        self.play(Create(box))
        sum_0 = MT(r"2.^1{0} \; ^1{1} \icat^3 6").next_to(line, DOWN, buff=0.3)
        sum_0.align_to(addition_stack, RIGHT)  # Align the whole block to the stack
        sum_0.set_opacity(0)  # Hide it initially
        self.add(sum_0)
        _i_map = {
            3: slice(4, 6),
            2: slice(2, 4),
            6: 8,
            slice(4, 6): slice(6, 8)
        }
        animate_sum_steps(self, n1, n2, sum_0, box, [6, slice(4, 6), 3, 2, (0, 1)], t_slice_map=_i_map)
        self.play(Uncreate(box))
        self.wait()

        # perform the carries
        arrow = CurvedArrow(
                sum_0[0][4].get_top() + LEFT*0.1,
                sum_0[0][3].get_top() + UP*0.2 + LEFT*0.05,
                angle=TAU/2.5,
                tip_length=0.08
        ).set_stroke(width=3).set_color(YELLOW)
        arrow.rotate(PI/4)
        def move_carry_arrow(target_idx):
            return arrow.animate.move_to(
                sum_0[0][target_idx].get_top() + LEFT*0.1 + UP*0.1
            )
        self.play(FadeOut(line), self.camera.frame.animate.set_width(3).move_to(sum_0))
        self.play(Create(arrow))
        self.wait()
        self.play(move_carry_arrow(2), sum_0.animate.become(MT(r"2.^1{1} 1 \icat^3 6").move_to(sum_0)), run_time=2)
        self.wait()
        self.play(FadeOut(arrow), sum_0.animate.become(MT(r"3.11 \icat^3 6").move_to(sum_0)), run_time=2)
        self.wait()
        self.play(Indicate(sum_0[0][3:5], color=BLUE))
        self.play(sum_0.animate.become(MT(r"3.\icat^2 1 \icat^3 6").move_to(sum_0)))
        self.wait()
        self.play(FadeIn(line), self.camera.frame.animate.set_width(14).move_to(ORIGIN))
        
        # final answer
        final_group = VGroup(sum_0, addition_group, box)
        self.play(final_group.animate.center().scale(1.2))
        self.play(Circumscribe(final_group, color=GREEN, time_width=1, buff=0.4), run_time=3)

        self.wait(5)
