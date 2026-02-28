from manim import *
import numpy as np

class GeneratedVideo(Scene):
    def construct(self):
        title = Text("Dijkstra Algorithm").to_edge(UP)
        self.add(title)
        self.wait(5)

        nodes = VGroup(
            Dot().set_color(BLUE),
            Dot().set_color(BLUE),
            Dot().set_color(BLUE),
            Dot().set_color(BLUE),
            Dot().set_color(BLUE)
        ).arrange(RIGHT, buff=1)
        edges = VGroup(
            Line(nodes[0], nodes[1]),
            Line(nodes[1], nodes[2]),
            Line(nodes[2], nodes[3]),
            Line(nodes[3], nodes[4]),
            Line(nodes[0], nodes[3]),
            Line(nodes[1], nodes[4])
        )
        self.add(nodes, edges)
        self.wait(10)

        nodes[0].set_color(YELLOW)
        self.wait(2)
        nodes[1].set_color(YELLOW)
        self.wait(2)
        nodes[2].set_color(YELLOW)
        self.wait(2)
        nodes[3].set_color(YELLOW)
        self.wait(2)
        nodes[4].set_color(YELLOW)
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        title = Text("Dijkstra Algorithm").to_edge(UP)
        self.add(title)
        complexity = MathTex(r"O(|E| + |V| \log |V|)").to_edge(DOWN)
        self.add(complexity)
        self.wait(10)

        self.play(FadeOut(*self.mobjects))

        title = Text("Dijkstra Algorithm").to_edge(UP)
        self.add(title)
        complexity = MathTex(r"O(n \log n)").to_edge(DOWN)
        self.add(complexity)
        self.wait(10)

        self.play(FadeOut(*self.mobjects))

        title = Text("Dijkstra Algorithm").to_edge(UP)
        self.add(title)
        complexity = MathTex(r"O(n)").to_edge(DOWN)
        self.add(complexity)
        self.wait(5)

        complexity = MathTex(r"O(\log n)")
        self.play(Transform(complexity, complexity))
        self.wait(5)

        complexity = MathTex(r"O(n \log n)")
        self.play(Transform(complexity, complexity))
        self.wait(10)

        self.play(FadeOut(*self.mobjects))