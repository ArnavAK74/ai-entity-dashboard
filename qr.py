import qrcode
from PIL import Image, ImageDraw

# Generate QR code
url = "https://ai-entity-dashboard-etpfujqszfznptatq9b34b.streamlit.app/"
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(url)
qr.make()
img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
draw = ImageDraw.Draw(img)

# Define pixel letters L I A with spacing
L = [[1,0],[1,0],[1,0],[1,0],[1,1]]
I = [[1],[1],[1],[1],[1]]
A = [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]]

# Combine with 2-pixel spacing
letters = []
for i in range(5):
    letters.append(L[i] + [0,0] + I[i] + [0,0] + A[i])

# Drawing setup
block = 6  # size of each pixel block
width = len(letters[0]) * block
height = len(letters) * block
img_w, img_h = img.size
start_x = (img_w - width) // 2
start_y = (img_h - height) // 2

# 🔲 1. Draw a white rectangle background behind "LIA"
padding = 4
draw.rectangle(
    [start_x - padding, start_y - padding, start_x + width + padding, start_y + height + padding],
    fill="white"
)

# 🖊️ 2. Draw the black pixel-art "LIA"
for row_idx, row in enumerate(letters):
    for col_idx, val in enumerate(row):
        if val == 1:
            x0 = start_x + col_idx * block
            y0 = start_y + row_idx * block
            draw.rectangle([x0, y0, x0 + block - 1, y0 + block - 1], fill="black")

# Save result
img.save("qr_with_clear_lia.png")
print("✅ QR with centered visible 'LIA' saved as 'qr_with_clear_lia.png'")
