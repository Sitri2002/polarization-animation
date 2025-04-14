from manim import *

class Circular(ThreeDScene):
    def construct(self):
        # Set camera orientation for a clear 3D view
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES, frame_center=[1,0.6,1])
        # Set zoom to ensure the entire scene is visible
        self.camera.set_zoom(0.3)
        label = Tex("Circularly Polarized Light",font_size=10, color=RED)
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

        def get_horizontal_wave():
            return ParametricFunction(
                lambda u: np.array([u, np.sin(u - h_tracker.get_value()), 0 ]),
                t_range=[-12.5, 10],
                color=YELLOW,
                stroke_width=1
            )
        
        hori_wave = always_redraw(get_horizontal_wave)

        self.add(vert_wave)
        self.add(hori_wave)

        self.play(Write(label), run_time = 0.5)
        self.play([v_tracker.animate.set_value(20),h_tracker.animate.set_value(20)], run_time=5, rate_func=linear)