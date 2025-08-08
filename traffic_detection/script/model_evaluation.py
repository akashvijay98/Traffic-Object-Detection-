import os
from pycocotools.coco import COCO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Configuration ---
dataDir = '/path/to/your/coco2017' # IMPORTANT: Change this to your actual path
dataType = 'val2017'
annFile = os.path.join(dataDir, 'annotations', f'instances_{dataType}.json')
imgDir = os.path.join(dataDir, dataType)

# --- Initialize COCO API ---
coco = COCO(annFile)

# --- Get image IDs ---
imgIds = coco.getImgIds()
# Optionally, get a specific image ID
# imgIds = coco.getImgIds(imgIds = [324158]) # Example image ID

# --- Load and display an image with annotations ---
img = coco.loadImgs(imgIds[0])[0] # Load the first image
imgPath = os.path.join(imgDir, img['file_name'])
I = Image.open(imgPath).convert('RGB')

# Load annotations for this image
annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
anns = coco.loadAnns(annIds)

plt.imshow(I)
ax = plt.gca()

# Draw bounding boxes and masks
for ann in anns:
    # Bounding box [x,y,width,height]
    [x, y, w, h] = ann['bbox']
    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

    # Category name
    cat = coco.loadCats(ann['category_id'])[0]
    plt.text(x, y-5, cat['name'], color='red', fontsize=8, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # If you want to visualize masks, you'd need to use 'ann['segmentation']'
    # and either polygon or RLE decoding, which is more complex.
    # For example:
    # if 'segmentation' in ann and ann['iscrowd'] == 0:
    #     for seg in ann['segmentation']:
    #         if isinstance(seg, list): # Polygon
    #             poly = np.array(seg).reshape((len(seg)//2, 2))
    #             poly_patch = patches.Polygon(poly, closed=True, fill=True, facecolor='green', alpha=0.3)
    #             ax.add_patch(poly_patch)

plt.axis('off')
plt.show()

print(f"Loaded image: {img['file_name']}")
print(f"Annotations for this image: {len(anns)}")