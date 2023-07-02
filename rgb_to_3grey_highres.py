from UnityEngine import Texture, Shader, Material, ImageConversion, Debug
from UnityEditor import AssetDatabase, Selection, TextureImporter, TextureImporterPlatformSettings
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
        channels = image.split()[:3]
        r, g, b = channels

        # チャンネルをグレースケールに変換
        r_gray = r.convert('L')
        g_gray = g.convert('L')
        b_gray = b.convert('L')

        # 保存するファイル名を生成
        filename = os.path.splitext(texture_path)[0]  # 拡張子を除いたファイル名
        r_gray_filename = f"{filename}_01Channel.png"
        g_gray_filename = f"{filename}_02Channel.png"
        b_gray_filename = f"{filename}_03Channel.png"

        # グレースケール画像を保存
        r_gray.save(r_gray_filename)
        g_gray.save(g_gray_filename)
        b_gray.save(b_gray_filename)

        
        # 保存したグレースケール画像のテクスチャを読み込む
        r_gray_texture = AssetDatabase.LoadAssetAtPath(r_gray_filename, Texture)
        g_gray_texture = AssetDatabase.LoadAssetAtPath(g_gray_filename, Texture)
        b_gray_texture = AssetDatabase.LoadAssetAtPath(b_gray_filename, Texture)

        # テクスチャのインポーター設定を取得
        r_gray_importer = TextureImporter.GetAtPath(r_gray_filename)
        g_gray_importer = TextureImporter.GetAtPath(g_gray_filename)
        b_gray_importer = TextureImporter.GetAtPath(b_gray_filename)

        # Androidプラットフォームの設定を取得または作成
        r_gray_platform_settings = r_gray_importer.GetPlatformTextureSettings("Android")
        g_gray_platform_settings = g_gray_importer.GetPlatformTextureSettings("Android")
        b_gray_platform_settings = b_gray_importer.GetPlatformTextureSettings("Android")
        if r_gray_platform_settings is None:
            r_gray_platform_settings = TextureImporterPlatformSettings()
        if g_gray_platform_settings is None:
            g_gray_platform_settings = TextureImporterPlatformSettings()
        if b_gray_platform_settings is None:
            b_gray_platform_settings = TextureImporterPlatformSettings()

        # 解像度を512に設定
        r_gray_platform_settings.maxTextureSize = 512
        g_gray_platform_settings.maxTextureSize = 512
        b_gray_platform_settings.maxTextureSize = 512

        # Androidプラットフォームの設定を適用
        r_gray_importer.SetPlatformTextureSettings(r_gray_platform_settings)
        g_gray_importer.SetPlatformTextureSettings(g_gray_platform_settings)
        b_gray_importer.SetPlatformTextureSettings(b_gray_platform_settings)

        # インポーターの設定を反映
        r_gray_importer.SaveAndReimport()
        g_gray_importer.SaveAndReimport()
        b_gray_importer.SaveAndReimport()
    

            
        Debug.Log(f"テクスチャ '{texture_path}' のグレースケール画像を保存しました。")
        print("done : " + filename)

selected_textures = Selection.objects  # エディタ上で選択したテクスチャ

selected_texture_paths = [AssetDatabase.GetAssetPath(texture) for texture in selected_textures]
split_rgb_to_grayscale(selected_texture_paths)
