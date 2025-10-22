# Grove Lab Notebook: Full Interactive Dashboard (.ipynb version ready)

# ===== 1. Imports =====
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display, clear_output
import trimesh
from ipywidgets import VBox, HBox, Textarea, Button

# ===== 2. Sample Dataset =====
data = {
    'material_name': ['Material A', 'Material B', 'Material C', 'Material D', 'Material E'],
    'performance': [0.8, 0.6, 0.9, 0.5, 0.7],
    'sustainability': [0.7, 0.9, 0.5, 0.8, 0.6],
    'cost': [10, 20, 15, 25, 18],
    'stability': [0.9, 0.8, 0.7, 0.6, 0.85],
    'lifespan': [5, 7, 4, 6, 5],
    'cad_file': ['models/material_a.stl', 'models/material_b.stl', 'models/material_c.stl', 'models/material_d.stl', 'models/material_e.stl']
}

df = pd.DataFrame(data)
annotations = {}

# ===== 3. Weight Sliders =====
w_perf = widgets.FloatSlider(description='Performance', min=0, max=1, step=0.01, value=0.5)
w_sust = widgets.FloatSlider(description='Sustainability', min=0, max=1, step=0.01, value=0.5)

# ===== 4. Compute Weighted Score =====
def update_scores(perf_weight, sust_weight):
    df['score'] = df['performance']*perf_weight + df['sustainability']*sust_weight
    top_candidates = df.sort_values('score', ascending=False).head(5)
    return top_candidates

# ===== 5. 2D Tradeoff =====
def plot_tradeoff(top_candidates):
    fig = px.scatter(top_candidates,
                     x='performance', y='sustainability',
                     size='cost', color='stability',
                     hover_data=['material_name', 'lifespan'],
                     title='Tradeoff Visualizer')
    fig.update_layout(template='simple_white')
    return fig

# ===== 6. 3D CAD Simulation =====
def plot_3d_model(materials, animate_property=None):
    fig = go.Figure()
    for _, mat in materials.iterrows():
        try:
            mesh = trimesh.load(mat['cad_file'])
            x, y, z = mesh.vertices.T
            if animate_property:
                scale = mat[animate_property]
                z = z * scale
            fig.add_trace(go.Mesh3d(x=x, y=y, z=z, color='orange', opacity=0.5, name=mat['material_name']))
        except Exception as e:
            print(f"Failed to load {mat['cad_file']}: {e}")
    fig.update_layout(title='3D Material Simulation with CAD Import')
    return fig

# ===== 7. Annotations =====
annotation_text = Textarea(placeholder='Add notes for selected candidate', description='Notes:', layout=widgets.Layout(width='100%', height='100px'))
save_button = Button(description='Save Annotation')
selected_material = [df.iloc[0]['material_name']]

def save_annotation(b):
    material = selected_material[0]
    annotations[material] = annotation_text.value
    print(f"Saved annotation for {material}")

save_button.on_click(save_annotation)

# ===== 8. Dashboard =====
output_tradeoff = widgets.Output()
output_3d = widgets.Output()
output_annotations = widgets.Output()

def update_dashboard(change=None):
    top = update_scores(w_perf.value, w_sust.value)
    selected_material[0] = top.iloc[0]['material_name']
    with output_tradeoff:
        clear_output(wait=True)
        fig2d = plot_tradeoff(top)
        fig2d.show()
    with output_3d:
        clear_output(wait=True)
        fig3d = plot_3d_model(top, animate_property='performance')
        fig3d.show()
    with output_annotations:
        clear_output(wait=True)
        annotation_text.value = annotations.get(selected_material[0], '')
        display(annotation_text, save_button)

w_perf.observe(update_dashboard, names='value')
w_sust.observe(update_dashboard, names='value')

dashboard = VBox([
    HBox([w_perf, w_sust]),
    HBox([output_tradeoff, output_3d]),
    output_annotations
])
display(dashboard)

update_dashboard()

# ===== 9. Export Functions =====
def export_top_candidates(top):
    top.to_csv('top_candidates.csv', index=False)
    print('Exported top_candidates.csv')

def export_tradeoff_chart(top):
    fig = plot_tradeoff(top)
    fig.write_image('tradeoff_chart.png')
    print('Exported tradeoff_chart.png')

def export_annotations():
    pd.DataFrame(list(annotations.items()), columns=['material_name','notes']).to_csv('annotations.csv', index=False)
    print('Exported annotations.csv')
