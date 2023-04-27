import os
from UnityEngine import Texture, Shader, Material
from UnityEditor import AssetDatabase, Selection


def create_material(material_name):
    # create a new material with the given name
    new_material = Material(Shader.Find(
        "Silent/Filamented (Roughness setup)"))
    new_material.name = material_name

    # set the texture properties if they exist
    albedo_texture_path = "Assets/Textures/" + material_name + "_D.png"
    if AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture):
        new_material.SetTexture(
            "_MainTex", AssetDatabase.LoadAssetAtPath(albedo_texture_path, Texture))
        new_material.EnableKeyword("_NORMALMAP")
        normal_texture_path = "Assets/Textures/" + material_name + "_N.png"
        if AssetDatabase.LoadAssetAtPath(normal_texture_path, Texture):
            new_material.SetTexture(
                "_BumpMap", AssetDatabase.LoadAssetAtPath(normal_texture_path, Texture))

        roughness_texture_path = "Assets/Textures/" + material_name + "_R.png"
        if AssetDatabase.LoadAssetAtPath(roughness_texture_path, Texture):
            new_material.SetTexture("_SpecGlossMap", AssetDatabase.LoadAssetAtPath(
                roughness_texture_path, Texture))
            # new_material.SetFloat("_Smoothness", 0.5)

    # save the new material
    AssetDatabase.CreateAsset(
        new_material, "Assets/Materials/" + material_name + ".mat")
    AssetDatabase.SaveAssets()


# get the selected material objects
selected_objects = Selection.objects
for obj in selected_objects:
    if obj.GetType() == Material:
        # create a new material using the selected material object's name
        material_name = obj.name
        create_material(material_name)
