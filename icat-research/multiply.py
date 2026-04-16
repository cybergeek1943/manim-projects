from manim import *
from manim import MathTex as MT
import config  # to enable the I-Cat notation in all MathTex instances


class Multiply(Scene):
    def construct(self):
        title = Text("Multiplication", font_size=36).to_corner(UL, 0.5)
        self.add(title)

        # Create numbers
        n1 = MT('12121212').shift(UP)
        n2 = MT('46').shift(DOWN)
        self.play(Create(n1), Create(n2))
        self.wait()

        # show notes
        note = Text('We want to multiply these.', font_size=20);
        self.play(Create(note))
        self.wait()
        self.play(Transform(note, Text("Let's look at the I-Cat form.", font_size=20).move_to(note)))
        self.wait()

        # convert to icat form
        n1t = MT(r'\icat^4 (12)').move_to(n1)
        self.play(TransformMatchingShapes(n1, n1t))
        n1 = n1t
        self.wait()

        # move to multiply line
        num_stack = VGroup(n1, n2)
        self.play(
            n2.animate.next_to(n1[0][4], DOWN, aligned_edge=RIGHT, buff=0.5),
            FadeOut(note)
        )
        times_sign = MT(r'\times').next_to(n2, LEFT, buff=0.8)
        line = Line().scale_to_fit_width(num_stack.width + 1).next_to(num_stack, DOWN, buff=0.5)
        mult_group = VGroup(num_stack, times_sign, line)
        self.play(
            FadeIn(line),
            FadeIn(times_sign),
            mult_group.animate.move_to(UP*0.7),
            run_time=0.5
        )

        # prep note
        note = Text('Step 1: Prepare a new I-Cat', font_size=25).next_to(mult_group, DOWN, buff=0.8)
        note[:5].set_color(BLUE)
        note.to_edge(DOWN)
        self.play(Write(note))
        def update_step_note(new_text: str):
            return Transform(note, Text(new_text, font_size=25, t2c={'[:6]': BLUE}).move_to(note))
        
        # create the result I-Cat
        r = MT(r'\icat^4 (??)').next_to(mult_group, DOWN, buff=0.3)
        self.play(Create(r))
        self.play(update_step_note('Step 2: Populate the initial I-Cat'))
        
        # populate the initial I-Cat
        self.play(
            Indicate(n1[0][4]),
            Indicate(n2),
            rate_func=there_and_back_with_pause, run_time=1.5
        )
        rt = MT(r'\icat^4 (? \quad 2 \times 46 \;)').move_to(r)
        self.play(
            TransformMatchingShapes(r, rt),
            n1[0][4].copy().animate.move_to(rt[0][4]).set_opacity(0),
            n2.copy().animate.move_to(rt[0][6:8]).set_opacity(0)
        )
        self.wait(0.4)
        r = rt
        rt = MT(r'\icat^4 (? \quad 2 \times 46 = 92 \;)').move_to(r)
        self.play(TransformMatchingShapes(r, rt))
        self.wait(0.4)
        r = rt
        rt = MT(r'\icat^4 (? \; ^9{2})').move_to(r)
        self.play(TransformMatchingShapes(r, rt))
        self.play(
            Indicate(n1[0][3]),
            Indicate(n2),
            rate_func=there_and_back_with_pause, run_time=1.5
        )
        r = rt
        rt = MT(r'\icat^4 (\; 1 \times 46 \quad ^9{2})').move_to(r)
        self.play(
            TransformMatchingShapes(r, rt),
            n1[0][3].copy().animate.move_to(rt[0][3]).set_opacity(0),
            n2.copy().animate.move_to(rt[0][5:7]).set_opacity(0)
        )
        self.wait(0.4)
        r = rt
        rt = MT(r'\icat^4 (\; 1 \times 46 = 46 \quad ^9{2})').move_to(r)
        self.play(TransformMatchingShapes(r, rt))
        self.wait(0.4)
        r = rt
        rt = MT(r'\icat^4 (^4{6} \; ^9{2})').move_to(r)
        self.play(TransformMatchingShapes(r, rt))
        r = rt

        # prep note
        self.play(
            update_step_note('Step 3: We partially unpack using the U = M/C formula.'),
            FocusOn(r[0][0], color=BLUE)
        )
        self.play(
            FadeOut(mult_group),
            r.animate.center().scale(1.25)
        )
        self.wait(2)
        rt = MT(r'\icat^3 (^4{6} \; ^9{2}) \; ^4{6} \; ^9{2}').move_to(r)
        self.play(TransformMatchingShapes(r, rt), run_time=3)
        r = rt

        # ==== propogate the carries ====
        self.play(update_step_note('Step 4: We can now propogate the carries!'))
        self.wait(2)
        self.play(r.animate.shift(DOWN*0.4).scale(2))
        
        arrow = CurvedArrow(ORIGIN, ORIGIN).next_to(r, UP, aligned_edge=RIGHT)
        arrow_plus = MT('+').set_color(YELLOW).next_to(arrow, UP)

        def move_carry_arrow(a: int, b: int):
            return arrow.animate.become(
                _:=CurvedArrow(
                    r[0][a].get_top() + UP*0.2,
                    r[0][b].get_top() + UP*0.4 + LEFT*0.1,
                    angle=TAU/2.5,
                    tip_length=0.2,
                    stroke_width=4,
                    color=YELLOW
                )
            ), arrow_plus.animate.next_to(_, UP, buff=0.2)
        
        self.play(*move_carry_arrow(10, 9))
        rt = MT(r"\icat^3 (^4{6} \; ^9{2}) \; ^5{5} \; 2").move_to(r).match_height(r)
        self.play(  # we must make sure that no two characters get animated at once so must exclude the carries
            TransformMatchingShapes(VGroup(*[m for i, m in enumerate(r[0]) if i not in range(8, 11)]), rt),
            FadeOut(r[0][8:11]),
            run_time=2
        )
        r = rt

        # note how 5 stays the same
        self.play(*move_carry_arrow(8, 6))
        carry_note = Text('Note: the carry coming in must be the same going out!', font_size=25, color=LIGHT_GRAY).next_to(note, UP, buff=0.5)
        self.play(
            Indicate(r[0][8], scale_factor=1.3, rate_func=there_and_back_with_pause),
            Create(carry_note)
        )

        rt = MT(r"\icat^3 (^4{6} \; ^9{7}) 5 2").move_to(r).match_height(r)
        self.play(
            TransformMatchingShapes(VGroup(*[m for i, m in enumerate(r[0]) if i != 6]), rt),
            r[0][6].animate.set_opacity(0),
            run_time=2
        )
        r = rt

        self.play(*move_carry_arrow(5, 4))
        rt = MT(r"\icat^3 (^5{5} \; 7) 5 2").move_to(r).match_height(r)
        self.play(
            TransformMatchingShapes(VGroup(*[m for i, m in enumerate(r[0]) if i not in (8, 5) and i not in range(3, 5)]), rt),
            r[0][8].animate.set_opacity(0),
            FadeOut(r[0][5], shift=LEFT + DOWN),
            FadeOut(r[0][3:5]),
            run_time=2
        )
        r = rt

        self.play(FadeOut(arrow), FadeOut(arrow_plus))
        self.play(ReplacementTransform(carry_note, carry_note:=Text('Note: the carry going out must be the same coming in!', font_size=25, color=LIGHT_GRAY).move_to(carry_note)))
        self.play(
            Indicate(r[0][3], scale_factor=1.3, rate_func=there_and_back_with_pause),
            Indicate(carry_note),
        )
    
        rt = MT(r"5 \icat^3 (5 7) 5 2").move_to(r).match_height(r)
        self.play(
            TransformMatchingShapes(r, rt),
            run_time=2
        )
        r = rt

        self.play(
            r.animate.scale(0.5).move_to(DOWN),
            FadeIn(MT(r'46 \times \icat^4 (12)').move_to(UP)),
            FadeIn(MT('=')),
            FadeOut(carry_note),
            FadeOut(note),
            run_time=2
        )
        self.play(
            Circumscribe(r, time_width=1, color=GREEN, buff=0.4),
            run_time=3
        )

        self.wait(5)
