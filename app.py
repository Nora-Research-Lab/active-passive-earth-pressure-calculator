import gradio as gr
import matplotlib
matplotlib.use('Agg')
from active_passive_earth_pressure_calculator import compute_pressures, generate_plot

def calculate(c_prime, phi_deg, gamma, H, beta_deg, q):
    try:
        result = compute_pressures(c_prime, phi_deg, gamma, H, beta_deg, q)
        if 'error' in result:
            return result['error'], "", "", "", "", None
        fig = generate_plot(c_prime, phi_deg, gamma, H, beta_deg, q,
                            result['Ka'], result['Kp'], result['Pa'], result['Pp'])
        return (f"{result['Ka']:.2f}",
                f"{result['Kp']:.2f}",
                f"{result['Pa']:.2f}",
                f"{result['Pp']:.2f}",
                "",  # placeholder for status
                fig)
    except Exception as e:
        return f"Error: {str(e)}", "", "", "", "", None

with gr.Blocks(title="Active & Passive Earth Pressure Calculator") as demo:
    gr.Markdown("# Active & Passive Earth Pressure Calculator (Rankine Theory)")
    with gr.Row():
        with gr.Column():
            c_prime = gr.Number(label="Effective cohesion c' (kPa)", minimum=0, maximum=100, value=0)
            phi_deg = gr.Number(label="Effective friction angle φ' (deg)", minimum=0, maximum=45, value=30)
            gamma = gr.Number(label="Unit weight γ (kN/m³)", minimum=14, maximum=22, value=18)
            H = gr.Number(label="Wall height H (m)", minimum=1, maximum=20, value=5)
            beta_deg = gr.Number(label="Ground slope β (deg)", minimum=0, maximum=45, value=0)
            q = gr.Number(label="Surcharge q (kPa)", minimum=0, maximum=50, value=0)
        with gr.Column():
            calc_btn = gr.Button("Calculate", variant="primary")
    with gr.Row():
        ka_out = gr.Textbox(label="Active coefficient Ka")
        kp_out = gr.Textbox(label="Passive coefficient Kp")
        pa_out = gr.Textbox(label="Active thrust Pa (kN/m)")
        pp_out = gr.Textbox(label="Passive thrust Pp (kN/m)")
    status = gr.Textbox(label="Status", visible=False)
    plot = gr.Plot(label="Schematic wall profile and pressure distribution")
    calc_btn.click(
        fn=calculate,
        inputs=[c_prime, phi_deg, gamma, H, beta_deg, q],
        outputs=[ka_out, kp_out, pa_out, pp_out, status, plot]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
