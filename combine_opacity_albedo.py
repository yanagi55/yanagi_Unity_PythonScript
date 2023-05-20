###
### ORMやARMなどでグレースケールが結合されてる場合、Unity2019で扱いやすくするために、分割して保存する
###

from UnityEngine import Texture, Shader, Material, ImageConversion, Debug
from UnityEditor import AssetDatabase, Selection, TextureImporter
from PIL import Image
import io
import os


def combine_opacity_albedo(opacity_texture_path, albedo_texture_path, output_texture_path):
    # Opacityマスクを読み込む
    opacity_texture = AssetDatabase.LoadAssetAtPath(opacity_texture_path, Texture)

    # Albedo画像を読み込む
    albedo_texture = AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture)

    # 出力用のテクスチャを作成
    output_texture = Texture(albedo_texture.width, albedo_texture.height, TextureFormat.RGBA32, False)

    # ピクセルごとに結合処理を行う
    for x in range(albedo_texture.width):
        for y in range(albedo_texture.height):
            albedo_color = albedo_texture.GetPixel(x, y)
            opacity = opacity_texture.GetPixel(x, y).a

            # アルベド画像とOpacityマスクを結合
            combined_color = Color(albedo_color.r, albedo_color.g, albedo_color.b, opacity)

            # 出力用テクスチャにピクセルを設定
            output_texture.SetPixel(x, y, combined_color)

    # テクスチャを適用し、ファイルとして保存
    output_texture.Apply()
    AssetDatabase.CreateAsset(output_texture, output_texture_path)
    AssetDatabase.SaveAssets()

    Debug.Log(f"Opacityマスクとアルベド画像を結合し、テクスチャ '{output_texture_path}' として保存しました。")

# 使用例
opacity_texture_path = "Assets/OpacityMask.png"  # Opacityマスクのパス
albedo_texture_path = "Assets/AlbedoTexture.png"  # Albedo画像のパス
output_texture_path = "Assets/CombinedTexture.png"  # 結合後のテクスチャの保存先パス
combine_opacity_albedo(opacity_texture_path, albedo_texture_path, output_texture_path)