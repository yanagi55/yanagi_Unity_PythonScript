import os
from UnityEngine import Texture, Shader, Material
from UnityEditor import AssetDatabase, Selection
import shutil

def create_material(material_name):
    # create a new material with the given name
    new_material = Material(Shader.Find("Silent/Filamented (Roughness setup)"))
    new_material.name = material_name


    # set the texture properties if they exist

    albedo_texture_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((AssetDatabase.GetAssetPath(Selection.activeObject))))), "Textures")
    albedo_texture_path = os.path.join(albedo_texture_dir, "T" + material_name[2:] + "_D.png")
    
    normal_texture_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((AssetDatabase.GetAssetPath(Selection.activeObject))))), "Textures")
    normal_texture_path = os.path.join(albedo_texture_dir, "T" + material_name[2:] + "_N.png")

    roughness_texture_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((AssetDatabase.GetAssetPath(Selection.activeObject))))), "Textures")
    roughness_texture_path = os.path.join(albedo_texture_dir, "T" + material_name[2:] + "_R.png")


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
    asset_path = (os.path.dirname((AssetDatabase.GetAssetPath(Selection.activeObject))))
    if not os.path.exists(asset_path):
        os.makedirs(asset_path)
    AssetDatabase.CreateAsset(
        new_material, os.path.join(asset_path, material_name + ".mat"))
    AssetDatabase.SaveAssets()
    print(asset_path + "/" + material_name)


# get the selected material objects
selected_objects = Selection.objects
for obj in selected_objects:
    if obj.GetType() == Material:
        material_name = obj.name

        # create a backup of the original material
        asset_path = AssetDatabase.GetAssetPath(obj)
        backup_path = os.path.join(os.path.dirname(asset_path), "Backup")
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        shutil.copy(asset_path, os.path.join(backup_path, material_name + ".mat"))
        
        # create a new material using the selected material object's name
        create_material(material_name)