import numpy as np

import matplotlib.pyplot as plt

class GraphGenerator:
    def __init__(self):
        pass

    def generate_donut_chart(self, username, data, colors=None, background_color='Black', text_color='White', wedgeprops=None):
        if not isinstance(data, dict):
            raise ValueError("Data should be a dictionary")

        labels = list(data.keys())
        sizes = list(data.values())
        title = f"{username}'s top languages"
        if colors is None:
            colors = plt.cm.Paired(np.linspace(0, 1, len(labels)))

        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, autopct='%1.1f%%',
                                          startangle=140, pctdistance=0.85, wedgeprops=wedgeprops)

        centre_circle = plt.Circle((0, 0), 0.70, fc=background_color)
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')
        plt.setp(autotexts, size=12, color=text_color)
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)

        legend = ax.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12, title_fontsize=14, facecolor=background_color, edgecolor=text_color, frameon=False)
        plt.setp(legend.get_title(), color=text_color)
        plt.setp(legend.get_texts(), color=text_color)
        plt.title(title, fontsize=16, color=text_color)
        plt.tight_layout(rect=[0, 0, 0.75, 1]) 
        plt.show()