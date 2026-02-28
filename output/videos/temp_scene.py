from manim import *
import numpy as np

class GeneratedVideo(Scene):
    def construct(self):
        title = Text("Redux in React", font_size=48, color=BLUE).to_edge(UP)
        self.add(title)
        self.wait(4)

        main = Rectangle(width=6, height=4, color=BLUE, fill_opacity=0.5).move_to(ORIGIN)
        self.add(main)
        self.wait(2)

        store_text = Text("Store", font_size=24, color=GREEN).move_to(main.get_center())
        self.add(store_text)
        self.wait(2)

        reducer_text = Text("Reducer", font_size=24, color=YELLOW).next_to(main, DOWN)
        self.add(reducer_text)
        self.wait(2)

        action_text = Text("Action", font_size=24, color=RED).next_to(reducer_text, DOWN)
        self.add(action_text)
        self.wait(2)

        dispatch_text = Text("Dispatch", font_size=24, color=GREEN).next_to(action_text, DOWN)
        self.add(dispatch_text)
        self.wait(2)

        state_text = Text("State", font_size=24, color=BLUE).next_to(dispatch_text, DOWN)
        self.add(state_text)
        self.wait(2)

        formula = MathTex(r"State = Reducer(State, Action)").to_edge(DOWN)
        self.add(formula)
        self.wait(4)

        self.play(FadeOut(*self.mobjects))
        self.wait(2)

        new_title = Text("React-Redux", font_size=48, color=BLUE).to_edge(UP)
        self.add(new_title)
        self.wait(4)

        new_main = Rectangle(width=6, height=4, color=BLUE, fill_opacity=0.5).move_to(ORIGIN)
        self.add(new_main)
        self.wait(2)

        provider_text = Text("Provider", font_size=24, color=GREEN).move_to(new_main.get_center())
        self.add(provider_text)
        self.wait(2)

        connect_text = Text("Connect", font_size=24, color=YELLOW).next_to(new_main, DOWN)
        self.add(connect_text)
        self.wait(2)

        map_state_text = Text("Map State", font_size=24, color=RED).next_to(connect_text, DOWN)
        self.add(map_state_text)
        self.wait(2)

        map_dispatch_text = Text("Map Dispatch", font_size=24, color=GREEN).next_to(map_state_text, DOWN)
        self.add(map_dispatch_text)
        self.wait(2)

        new_formula = MathTex(r"Component = Connect(Map State, Map Dispatch)(Component)").to_edge(DOWN)
        self.add(new_formula)
        self.wait(10)

        self.play(FadeOut(*self.mobjects))
        self.wait(4)

        final_title = Text("Redux in React", font_size=48, color=BLUE).to_edge(UP)
        self.add(final_title)
        self.wait(4)

        final_main = Rectangle(width=6, height=4, color=BLUE, fill_opacity=0.5).move_to(ORIGIN)
        self.add(final_main)
        self.wait(2)

        final_text = Text("State Management", font_size=24, color=GREEN).move_to(final_main.get_center())
        self.add(final_text)
        self.wait(4)

        self.play(FadeOut(*self.mobjects))
        self.wait(4)