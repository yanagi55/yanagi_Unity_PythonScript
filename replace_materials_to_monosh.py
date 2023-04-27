import os
from UnityEngine import Texture, Shader, Material
from UnityEditor import AssetDatabase, Selection

def create_material(material_name):
    # create a new material with the given name
    new_material = Material(Shader.Find("Silent/Filamented (Roughness setup)"))
    new_material.name = material_name

    # set the texture properties if they exist
    albedo_texture_path = "Assets/SCANDINAVIAN_APMENT/Textures/T_wood_02_D.png"
    normal_texture_path = "Assets/SCANDINAVIAN_APMENT/Textures/T_wood_02_N.png"
    roughness_texture_path = "Assets/SCANDINAVIAN_APMENT/Textures/T_wood_02_R.png"
    if AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture):
        new_material.SetTexture(
            "_MainTex", AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture))
    if AssetDatabase.LoadAssetAtPath(normal_texture_path, Texture):
        new_material.SetTexture(
            "_BumpMap", AssetDatabase.LoadAssetAtPath(normal_texture_path, Texture))
    if AssetDatabase.LoadAssetAtPath(roughness_texture_path, Texture):
        new_material.SetTexture(
            "_SpecGlossMap", AssetDatabase.LoadAssetAtPath(roughness_texture_path, Texture))
    
    # Bakery Mode
    new_material.SetInt("_Bakery", 3) # Note: Filamented Standardで、[None, SH, RMN, MonoSH]になってる

    # save the new material
    asset_path = "Assets/SCANDINAVIAN_APMENT/Materials/INSTANCE/NewMaterials"
    if not os.path.exists(asset_path):
        os.makedirs(asset_path)
    AssetDatabase.CreateAsset(
        new_material, os.path.join(asset_path, material_name + ".mat"))
    AssetDatabase.SaveAssets()


# create a new material using the texture path provided
create_material("TestMaterial")