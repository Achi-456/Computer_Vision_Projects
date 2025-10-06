import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from IPython.display import display, Image as IPImage
import ipywidgets as widgets
from io import BytesIO
from PIL import Image


class HomographyCompositor:

    def __init__(self, source_img_path, dest_image_path):
        self.source_img = source_img_path
        self.dest_img = dest_image_path
        self.source_img = cv.imread(self.source_img)
        self.dest_img = cv.imread(self.dest_img)

        self.source_img_rgb = cv.cvtColor(self.source_img, cv.COLOR_BGR2RGB)
        self.dest_img_rgb = cv.cvtColor(self.dest_img, cv.COLOR_BGR2RGB)

        h, w = self.source_img_rgb.shape[:2]
        self.src_points = np.float32([
            [0,0],
            [w-1,0],
            [w-1,h-1],
            [0,h-1]
        ])

        # plot the source image and destination image
        fig, ax = plt.subplots(1,2, figsize=(12,6))
        ax[0].imshow(self.source_img_rgb)
        ax[0].set_title('Source Image')
        ax[0].axis('off')
        ax[1].imshow(self.dest_img_rgb)
        ax[1].set_title('Destination Image')
        ax[1].axis('off')
        plt.tight_layout()

        print(f"Source image loaded: {w}x{h}")
        print(f"Destination image loaded: {self.dest_img_rgb.shape[1]}x{self.dest_img_rgb.shape[0]}")

    def select_destination_points(self):
        self.dest_points = []
        self.fig, self.ax = plt.subplots(1,1,figsize=(12,8))
        self.ax.imshow(self.dest_img_rgb)
        self.ax.set_title('Select 4 points in the destination image')
        self.ax.axis('off')

        def onclick(event):
            if event.xdata is not None and event.ydata is not None:
                if len(self.dest_points) < 4:
                    x,y = event.xdata, event.ydata
                    self.dest_points.append([x,y])

                    # Draw point
                    circle = Circle((x,y), 5, color='red', fill=True ,zorder=5)
                    self.ax.add_patch(circle)
                    self.ax.text(x, y-15, str(len(self.dest_points)), 
                            color='yellow', fontsize=16, fontweight='bold',
                            ha='center', bbox=dict(boxstyle='circle', facecolor='red'))

                    # Draw line connecting points
                    if len(self.dest_points) > 1:
                        pts = np.array(self.dest_points)
                        self.ax.plot([pts[-2, 0], pts[-1, 0]], 
                                [pts[-2, 1], pts[-1, 1]], 'r-', linewidth=3)

                    if len(self.dest_points) == 4:
                        pts = np.array(self.dest_points)
                        self.ax.plot([pts[-1, 0], pts[0, 0]], 
                                [pts[-1, 1], pts[0, 1]], 'r-', linewidth=3)
                        self.ax.set_title("✓ 4 points selected! Close window to continue.", 
                                        fontsize=14, fontweight='bold', color='green')
                        print("\n✓ All 4 points selected successfully!")
                    
                    self.fig.canvas.draw()
        self.fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()      



source_path_1 = 'images/aus.png'
dest_path_1 = 'images/cover-cricket2.png'
compositor = HomographyCompositor(source_path_1, dest_path_1)
compositor.select_destination_points()

