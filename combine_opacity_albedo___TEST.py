from UnityEngine import Texture2D, TextureFormat, Color
from UnityEditor import AssetDatabase, Selection, TextureImporter
import os
import sys

def combine_opacity_albedo(opacity_texture_path, albedo_texture_path, output_texture_path):
    # Opacityマスクのテクスチャをインポート
    opacity_texture = AssetDatabase.LoadAssetAtPath(opacity_texture_path, Texture2D)
    opacity_pixels = opacity_texture.GetPixels()

    # Albedo画像のテクスチャをインポート
    albedo_texture = AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture2D)
    albedo_pixels = albedo_texture.GetPixels()

    # ピクセルごとに結合処理を行う
    combined_pixels = []
    for i in range(len(albedo_pixels)):
        albedo_color = albedo_pixels[i]
        opacity = opacity_pixels[i].a

        # アルベド画像とOpacityマスクを結合
        combined_color = Color(albedo_color.r, albedo_color.g, albedo_color.b, opacity)

        combined_pixels.append(combined_color)

    # 出力用のテクスチャを作成
    output_texture = Texture2D(albedo_texture.width, albedo_texture.height, TextureFormat.RGBA32, False)
    output_texture.SetPixels(combined_pixels)
    output_texture.Apply()

    # テクスチャのインポート設定を取得
    importer = TextureImporter.GetAtPath(output_texture_path)  # 出力先テクスチャのインポーター

    if importer is None:
        print("指定されたテクスチャは存在しません。")
        return

    # インポート設定の変更
    importer.isReadable = True  # 読み書き可能にする
    importer.textureCompression = TextureImporterCompression.Uncompressed  # 圧縮なし
    importer.SaveAndReimport()

    # テクスチャをファイルとして保存
    bytes = output_texture.EncodeToPNG()
    File.WriteAllBytes(output_texture_path, bytes)

    print(f"Opacityマスクとアルベド画像を結合し、テクスチャ '{output_texture_path}' として保存しました。")

# 使用例
opacity_texture_path = "Assets/OpacityMask.png"  # Opacityマスクのパス
albedo_texture_path = "Assets/AlbedoTexture.png"  # Albedo画像のパス
output_texture_path = "Assets/CombinedTexture.png"  # 結合後のテクスチャの保存先パス
combine_opacity_albedo(opacity_texture_path, albedo_texture_path, output_texture_path)
