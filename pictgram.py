from PIL import Image
import os
import random

# 入力フォルダと出力画像のファイル名を指定します
input_folder = "images/"  # 画像が格納されているフォルダ
output_image = "output.png"  # 出力画像のファイル名
square_size = 100  # 画像をリサイズする正方形のサイズ
grid_columns = 4  # グリッドの列数

# 画像をロードし、正方形にリサイズする関数
def make_square(image, size):
    width, height = image.size
    new_image = Image.new("RGBA", (size, size), (255, 255, 255, 0))  # 透明な背景 (RGBA)
    ratio = min(size / width, size / height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    offset = ((size - new_width) // 2, (size - new_height) // 2)
    new_image.paste(resized_image, offset, resized_image)  # 第3引数を指定して透明度を維持
    return new_image

# 画像をランダムな順番でグリッドに配置する関数
def create_random_grid(input_folder, square_size, grid_columns):
    images = []
    valid_extensions = (".png", ".jpg", ".jpeg")
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            try:
                img = Image.open(os.path.join(input_folder, filename))
                img = img.convert("RGBA")  # PNGの透明度を保持する
                img_square = make_square(img, square_size)
                images.append(img_square)
            except Exception as e:
                print(f"Error loading image {filename}: {e}")

    # 画像の順番をランダムにシャッフル
    random.shuffle(images)

    num_images = len(images)
    grid_rows = (num_images + grid_columns - 1) // grid_columns  # 行数を計算

    # キャンバスを作成（透明な背景）
    canvas_width = square_size * grid_columns
    canvas_height = square_size * grid_rows
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))

    # グリッドに画像を配置
    for i, img in enumerate(images):
        row = i // grid_columns
        col = i % grid_columns
        x = col * square_size
        y = row * square_size
        canvas.paste(img, (x, y), img)  # 第3引数で透明度を維持

    return canvas

# ランダムに配置されたグリッド画像を作成し保存
canvas_image = create_random_grid(input_folder, square_size, grid_columns)
canvas_image.save(output_image)
print(f"出力画像を{output_image}に保存しました。")
