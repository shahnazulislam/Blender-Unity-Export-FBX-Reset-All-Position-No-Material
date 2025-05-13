# Такс, нужно поставить цель, ото что-то код не идет(
# Цель - Экспорт fbx с геометрией по центру и без материалов.
# Лапками влом.

import bpy
import os
import mathutils

# :D Папка для экспорта FBX (рядом с .blend файлом в общем :3)
# Пока прям в unity пусть валяется
export_folder = bpy.path.abspath("//ExportedFBX")
os.makedirs(export_folder, exist_ok=True)

# Временные объекты для удаления ===
temp_objects = []

for obj in bpy.context.selected_objects:
    if obj.type != 'MESH':
        continue

    # Копируем объект и его меш ===
    obj_copy = obj.copy()
    obj_copy.data = obj.data.copy()

    # Удаляем все материалы у копии
    obj_copy.data.materials.clear()

    # Добавляем копию в сцену ===
    bpy.context.collection.objects.link(obj_copy)

    # Активируем копию ===
    bpy.context.view_layer.objects.active = obj_copy
    bpy.ops.object.select_all(action='DESELECT')
    obj_copy.select_set(True)

    # Перемещаем вершины к центру ===
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=[-obj_copy.location.x, -obj_copy.location.y, -obj_copy.location.z])
    bpy.ops.object.mode_set(mode='OBJECT')

    # Ставим origin по геометрии и применяем трансформы ===
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Перемещаем в (0,0,0) ===
    obj_copy.location = (0, 0, 0)

    # Добавляем во временный список ===
    temp_objects.append(obj_copy)

    # Путь к файлу FBX ===
    export_path = os.path.join(export_folder, f"{obj.name}_centered.fbx")

    # Самая мякотка!
    # Экспорт ===
    bpy.ops.export_scene.fbx(
        filepath=export_path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        bake_space_transform=True,
        object_types={'MESH'},
        mesh_smooth_type='OFF',
        use_mesh_modifiers=True,
        add_leaf_bones=False,
        path_mode='COPY'
    )

# Удаляем временные объекты из сцены ===
bpy.ops.object.select_all(action='DESELECT')
for temp in temp_objects:
    temp.select_set(True)
bpy.ops.object.delete()

# TODO: В файл потом лучше логировать.
print(f":3 Экспорт с геометрией по центру и без материалов завершён: {export_folder}")
