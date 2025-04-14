from manim import *

class SineWave3D(ThreeDScene):
    def construct(self):
        # Set camera orientation for a clear 3D view
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES, frame_center=[1,0.6,1])
        # Set zoom to ensure the entire scene is visible
        self.camera.set_zoom(0.3)
        label = Tex("Linearly Polarized Light",font_size=10, color=RED)
        label.move_to([0, 1, 4])  # 3D position (x, y, z)
        self.add_fixed_in_frame_mobjects(label) 
        
        axes = ThreeDAxes(
            x_range=[0, 100, 10], y_range=[-5, 5, 3], z_range=[-5, 5, 3],
            x_length=25, y_length= 5, z_length=5,
            axis_config={"color": WHITE, "include_ticks": True, "include_numbers": False, "include_tip": False, "stroke_width": 1, "tick_size": 0.05},
        )
        # Switch x / z label
        # axes_labels = axes.get_axis_labels(
        #     Text("z").set_color(WHITE),
        #     Text("y").set_color(WHITE),
        #     Text("x").set_color(WHITE)
        # )
        self.add(axes)

        yz_plane = ComplexPlane(
            x_range=[-5, 5, 0.8],  # real axis → z-axis
            y_range=[-5, 5, 0.8],  # imag axis → y-axis
            background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.2, "stroke_width": 0.5},
            axis_config={"color": WHITE, "stroke_width": 0.5}
        ).scale(0.8)

        # Rotate so that x is fixed and it lies in the YZ plane
        yz_plane.rotate(angle=90 * DEGREES, axis=DOWN)  # rotates from XY → YZ
        yz_plane.shift([-12.5, 0, 0])  # move to x = -12.5
        self.add(yz_plane)

        xy_plane = ComplexPlane(
            x_range=[-5, 5, 0.8], 
            y_range=[-5, 5, 0.8], 
            background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.2, "stroke_width": 0.5},
            axis_config={"color": WHITE, "stroke_width": 0.5}
        ).scale(0.8)

        xy_plane.rotate(angle=0 * DEGREES, axis=UP)  
        xy_plane.shift([-7.5, 0, 0]) 
        self.add(xy_plane)

        v_tracker = ValueTracker(0)
        h_tracker = ValueTracker(0)
        
        # Vertical
        def get_vert_wave():
            return ParametricFunction(
                lambda u: np.array([u, 0, np.sin(u - v_tracker.get_value())]),
                t_range=[-12.5, 10],
                color=YELLOW,
                stroke_width=1
            )
        
        vert_wave = always_redraw(get_vert_wave)

        vert_dot = always_redraw(lambda: Dot(
        point=np.array([
            -12.5, 
            0, 
            np.sin(12.5-v_tracker.get_value())
        ]),
        color=RED,
        stroke_width=2,
        ))
        self.add(vert_wave)
        self.add(vert_dot)

        # Horizontal 
        def get_horizontal_wave():
            return ParametricFunction(
                lambda u: np.array([u, np.sin(u - h_tracker.get_value()), 0 ]),
                t_range=[-12.5, 10],
                color=YELLOW,
                stroke_width=1
            )
        
        hori_wave = always_redraw(get_horizontal_wave)
        
        
        hori_dot = always_redraw(lambda: Dot(
        point=np.array([
            -12.5, 
            np.sin(12.5-h_tracker.get_value()),
            0, 
        ]),
        color=RED,
        stroke_width=2,
        ))

        radius = 1
        yz_circle = ParametricFunction(
            lambda theta: np.array([
                -12.5,                      # x = constant (lies on yz-plane)
                radius * np.cos(theta),  # y
                radius * np.sin(theta)   # z
            ]),
            t_range=[0, TAU],
            color=BLUE,
            stroke_width=1
        )

        # self.add(yz_circle)

        

        vert_line = Line(
            start =[-12.5, 0, -1],
            end =[-12.5, 0, 1],
            color=BLUE,
            stroke_width=1
        )
        self.add(vert_line)

        hori_line = Line(
            start =[-12.5, -1, 0],
            end =[-12.5, 1, 0],
            color=BLUE,
            stroke_width=1
        )

        # Animate the wave propagation
        self.play(Write(label), run_time = 0.5)
        self.play(v_tracker.animate.set_value(20), run_time=5, rate_func=linear)
        self.play([Transform(vert_wave, hori_wave),Transform(vert_line, hori_line), Transform(vert_dot, hori_dot)], run_time=0.5)
        self.remove(vert_wave)
        self.remove(vert_dot)
        self.add(hori_wave)
        self.add(hori_dot)
        self.play(h_tracker.animate.set_value(20), run_time=5, rate_func=linear)
        
        