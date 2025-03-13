import numpy as np
import matplotlib.pyplot as plt
import io

class GraphGenerator:
    def __init__(self):
        pass

    def generate_donut_chart(self, title, data, colors=None, background_color='#252934', text_color='White', wedgeprops=None):
        if not isinstance(data, dict):
            raise ValueError("Data should be a dictionary")

        labels = list(data.keys())
        sizes = list(data.values())
        title
        if colors is None:
            colors = plt.cm.Paired(np.linspace(0, 1, len(labels)))

        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, autopct='%1.1f%%',
                                          startangle=140, pctdistance=0.85, wedgeprops=wedgeprops)

        centre_circle = plt.Circle((0, 0), 0.70, fc=background_color)
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')
        plt.setp(autotexts, size=12, color=text_color)
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)

        legend = ax.legend(wedges, labels, title="Languages", loc="center right", bbox_to_anchor=(-0.1, 0.5), fontsize=12, title_fontsize=14, frameon=False)
        plt.setp(legend.get_title(), color=text_color)
        plt.setp(legend.get_texts(), color=text_color)

        plt.title(title, fontsize=16, color=text_color)

        plt.tight_layout(rect=[0.2, 0, 1, 1]) 

        svg_buffer = io.StringIO()
        plt.savefig(svg_buffer, format='svg', bbox_inches='tight', pad_inches=0.1)
        svg_content = svg_buffer.getvalue()
        svg_buffer.close()

        plt.close(fig)

        return svg_content