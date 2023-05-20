from UnityEngine import Texture, Shader, Material, ImageConversion, Debug
from UnityEditor import AssetDatabase, Selection, TextureImporter
from PIL import Image
import io
import os

def split_rgb_to_grayscale(selected_textures):
    for texture_path in selected_textures:
        # テクスチャを読み込む
        texture = AssetDatabase.LoadAssetAtPath(texture_path, Texture)

        # テクスチャが読み書き可能でない場合はチェックを入れる
        if not TextureImporter.GetAtPath(texture_path).isReadable:
            TextureImporter.GetAtPath(texture_path).isReadable = True
            AssetDatabase.ImportAsset(texture_path)

        # テクスチャをバイト配列に変換
        texture_data = ImageConversion.EncodeToPNG(texture)

        # バイト配列をPILイメージに変換
        image = Image.open(io.BytesIO(texture_data))

        # R、G、Bのチャンネルに分割
        r, g, b = image.split()

        # チャンネルをグレースケールに変換
        r_gray = r.convert('L')
        g_gray = g.convert('L')
        b_gray = b.convert('L')

        # 保存するファイル名を生成
        filename = os.path.splitext(texture_path)[0]  # 拡張子を除いたファイル名
        r_gray_filename = f"{filename}_R.png"
        g_gray_filename = f"{filename}_G.png"
        b_gray_filename = f"{filename}_B.png"

        # グレースケール画像を保存
        r_gray.save(r_gray_filename)
        g_gray.save(g_gray_filename)
        b_gray.save(b_gray_filename)

        Debug.Log(f"テクスチャ '{texture_path}' のグレースケール画像を保存しました。")
        print("done : " + filename)

selected_textures = Selection.objects  # エディタ上で選択したテクスチャのリスト
selected_texture_paths = [AssetDatabase.GetAssetPath(texture) for texture in selected_textures]
split_rgb_to_grayscale(selected_texture_paths)
