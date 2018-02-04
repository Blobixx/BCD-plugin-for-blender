bl_info = {
    "name": "BCD Denoiser",
    "category": "Render",
}

import bpy
from bpy.types import (
        Panel,
        Menu,
        Operator,
        )
from bpy.props import (BoolProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty,
                       PointerProperty,
                       StringProperty)
from bl_operators.presets import AddPresetBase
import os


# class BCDDenoiserProperties(bpy.types.PropertyGroup):
#     # cls = bpy.types.SceneRenderLayer.cycles
#     bcd_denoiser_histogram_path_distance_threshold = FloatProperty(
#                 name="Threshold",
#                 description="Histogram patch distance threshold",
#                 default=1.0,
#         )
#     bcd_denoiser_radius_search_windows = IntProperty(
#             name="Radius Windows",
#             description="Radius of search windows",
#             default=6,
#     )
#     bcd_denoiser_random_pixel_order = BoolProperty(
#             name="Random Pixel Order",
#             description="random pixel order (in case of grid artifacts)",
#             default=False,
#     )
#     bcd_denoiser_radius_patches = IntProperty(
#             name="Radius of patches",
#             description="Radius of patches",
#             default=1,
#     )
#     bcd_denoiser_spike_filtering = BoolProperty(
#             name="Spike fiiltering",
#             description="Spike removal prefiltering",
#             default=False,
#     )
#     bcd_denoiser_factor = FloatProperty(
#             name="Factor",
#             description="Factor that is multiplied by standard deviation to get the threshold for classifying spikes during prefiltering. Put lower value to remove more spikes",
#             default=2.0,
#     )
#     bcd_denoiser_skipping_probability = FloatProperty(
#             name="Skipping probability",
#             description="Probability of skipping marked centers of denoised patches. 1 accelerates a lot the computations. 0 helps removing potential grid artifacts",
#             min=0.0, max=1.0,
#             default=1.0,
#     )
#     bcd_denoiser_scales = IntProperty(
#             name="Scales",
#             description="Number of Scales for Multi-Scaling",
#             default=3,
#     )
#     bcd_denoiser_use_cuda = BoolProperty(
#             name="Use Cuda",
#             description="Number of Scales for Multi-Scaling",
#             default=1,
#     )
#     bcd_denoiser_nb_cores= IntProperty(
#             name="Number of cores",
#             description="Number of cores used by OpenMP",
#             default=2,
#     )
#     bcd_denoiser_eigen_value = FloatProperty(
#             name="Eigen Value",
#             description="Minimum eigen value for matrix inversion",
#             default=0.00000001,
#     )

class CYCLES_MT_bcd_denoising_presets(Menu):
    bl_label = "BCD Presets"
    preset_subdir = "cycles/bcd"
    preset_operator = "script.execute_preset"
    COMPAT_ENGINES = {'CYCLES'}
    draw = Menu.draw_preset

class AddPresetBcd(AddPresetBase, Operator):
    '''Add a Sampling Preset'''
    bl_idname = "render.cycles_bcd_preset_add"
    bl_label = "Add BCD Preset"
    preset_menu = "CYCLES_MT_bcd_denoising_presets"

    preset_defines = [
        "layers = bpy.context.scene.render.layers.active.cycles"
    ]

    preset_values = [
        "layers.bcd_denoising_histogram_path_distance_threshold",
        "layers.bcd_denoising_radius_search_windows",
        "layers.bcd_denoising_radius_patches",
        "layers.bcd_denoising_factor",
        "layers.bcd_denoising_spike_filtering",
        "layers.bcd_denoising_eigen_value",
        "layers.bcd_denoising_random_pixel_order",
        "layers.bcd_denoising_use_cuda",
        "layers.bcd_denoising_skipping_probability",
        "layers.bcd_denoising_scales",
        "layers.bcd_denoising_nb_cores",
    ]

    preset_subdir = "cycles/bcd"


class CYCLES_RENDER_PT_bcd_denoising(bpy.types.Panel):
    bl_label = "BCD Denoiser"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render_layer"

    is_left = True

    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text="", icon="PHYSICS")
    def draw_header(self, context):
        rd = context.scene.render
        rl = rd.layers.active
        crl = rl.cycles
        cscene = context.scene.cycles
        layout = self.layout

        layout.prop(crl, "bcd_denoise", text="")


    def draw(self, context):
        layout = self.layout

        scene = context.scene
        cscene = scene.cycles
        rd = scene.render
        rl = rd.layers.active
        crl = rl.cycles

        layout.active = crl.bcd_denoise

        row = layout.row(align=True)
        row.menu("CYCLES_MT_bcd_denoising_presets", text=bpy.types.CYCLES_MT_bcd_denoising_presets.bl_label)
        row.operator("render.cycles_bcd_preset_add", text="", icon="ZOOMIN")
        row.operator("render.cycles_bcd_preset_add", text="", icon="ZOOMOUT").remove_active = True

        # layout.prop(crl, "bcd_executable_path", text="Path to BCD executable")
        split = layout.split()
        col = split.column()
        col.prop(crl, "bcd_denoising_histogram_path_distance_threshold", text="Path Threshold")
        col.prop(crl, "bcd_denoising_radius_search_windows", text="Radius Search Windows")
        col.prop(crl, "bcd_denoising_radius_patches")
        col.prop(crl, "bcd_denoising_factor", text="Factor")
        col.prop(crl, "bcd_denoising_skipping_probability", text="Skipping")
        col.prop(crl, "bcd_denoising_eigen_value")

        col = split.column()
        col.prop(crl, "bcd_denoising_random_pixel_order")
        col.prop(crl, "bcd_denoising_use_cuda")
        col.prop(crl, "bcd_denoising_spike_filtering")
        col.prop(crl, "bcd_denoising_scales")
        col.prop(crl, "bcd_denoising_nb_cores", text="Cores")

        layout.prop(crl, "bcd_denoised_path", text="Save image to")
        row = layout.row()
        row.operator("cycles.bcd_denoise", text="View Denoised Image")


class CYCLES_RENDER_OT_bcd_denoising(bpy.types.Operator):
    bl_label = "Bcd Operator"
    bl_idname = "cycles.bcd_denoise"
    bl_description = "Denoise render image"

    def execute(self, context):
        scene = context.scene
        cscene = scene.cycles
        rd = scene.render
        rl = rd.layers.active
        crl = rl.cycles
        #bpy.ops.render.render()
        # bcdpath = crl.bcd_executable_path
        # color =  "/Users/Shane/Documents/PRIM/bcd/test_denoising.exr"
        # hist = "/Users/Shane/Documents/PRIM/bcd/test_denoising_hist.exr"
        # cov = "/Users/Shane/Documents/PRIM/bcd/test_denoising_cov.exr"
        # denoised = "/Users/Shane/Documents/PRIM/bcd/test_denoised.exr"
        # color =  "/tmp/test_denoising.exr"
        # hist = "/tmp/test_denoising_hist.exr"
        # cov = "/tmp/test_denoising_cov.exr"
        denoised = crl.bcd_denoised_path
        denoised += "denoised.exr"
#         bcd_denoising_histogram_path_distance_threshold = crl.bcd_denoising_histogram_path_distance_threshold
#         bcd_denoising_radius_search_windows = crl.bcd_denoising_radius_search_windows
#         bcd_denoising_radius_patches = crl.bcd_denoising_radius_patches
#         bcd_denoising_factor = crl.bcd_denoising_factor
#         bcd_denoising_spike_filtering = crl.bcd_denoising_spike_filtering
#         bcd_denoising_eigen_value = crl.bcd_denoising_eigen_value
#         bcd_denoising_random_pixel_order = crl.bcd_denoising_random_pixel_order
#         bcd_denoising_use_cuda = crl.bcd_denoising_use_cuda
#         bcd_denoising_skipping_probability = crl.bcd_denoising_skipping_probability
#         bcd_denoising_scales = crl.bcd_denoising_scales
#         bcd_denoising_nb_cores = crl.bcd_denoising_nb_cores
# #        denoised2 = "/Users/Shane/Documents/PRIM/bcd/test_denoised2.exr"
#         bcd_denoising_spike_filtering = int(bcd_denoising_spike_filtering == 'true')
#         bcd_denoising_random_pixel_order = int(bcd_denoising_random_pixel_order == 'true')
#         bcd_denoising_use_cuda = int(bcd_denoising_use_cuda == 'true')

#         commandline = ""
#         commandline += bcdpath
#         commandline += " -i "
#         commandline += color
#         commandline += " -c "
#         commandline += cov
#         commandline += " -h "
#         commandline += hist
#         commandline += " -o "
#         commandline += denoised
#         commandline += " -d "
#         commandline += str(bcd_denoising_histogram_path_distance_threshold)
#         commandline += " -b "
#         commandline += str(bcd_denoising_radius_search_windows)
#         commandline += " -w "
#         commandline += str(bcd_denoising_radius_patches)
#         commandline += " -r "
#         commandline += str(bcd_denoising_random_pixel_order)
#         commandline += " -p "
#         commandline += str(bcd_denoising_spike_filtering)
#         commandline += " --p "
#         commandline += str(bcd_denoising_factor)
#         commandline += " -m "
#         commandline += str(bcd_denoising_skipping_probability)
#         commandline += " -s "
#         commandline += str(bcd_denoising_scales)
#         commandline += " -use-cuda "
#         commandline += str(bcd_denoising_use_cuda)
#         commandline += " -e "
#         commandline += str(bcd_denoising_eigen_value)
#         commandline += " --ncores "
#         commandline += str(bcd_denoising_nb_cores)
#         file = open("script.sh", "w")
#         # file.write("cd "+bcdpath+"\n")
#         file.write(commandline)
#         # print(commandline)
#         file.close()
#         os.system("chmod +x script.sh")
#         os.system("sh ./script.sh")
        # os.system(commandline)
        #os.system("./Users/Shane/Documents/PRIM/bcd/build/bcd_cli/bcd_cli -i /Users/Shane/Documents/PRIM/bcd/test_denoising.exr -h /Users/Shane/Documents/PRIM/bcd/test_denoising_hist.exr -c /Users/Shane/Documents/PRIM/bcd/test_denoising_cov.exr -o /Users/Shane/Documents/PRIM/bcd/test_denoised2.exr")
        img = bpy.data.images.load(denoised)
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

        # Change area type
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'IMAGE_EDITOR'
        area.spaces.active.image = img
        return {'FINISHED'}

classes = (
    CYCLES_MT_bcd_denoising_presets,
    AddPresetBcd,
    # BCDDenoiserProperties,
    CYCLES_RENDER_PT_bcd_denoising,
    CYCLES_RENDER_OT_bcd_denoising,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.SceneRenderLayer.bcd_denoiser = bpy.props.PointerProperty(type=BCDDenoiserProperties)
    # bpy.types.Scene.bcd_denoiser = PointerProperty(type=BCDDenoiserProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # del bpy.types.SceneRenderLayer.bcd_denoiser

if __name__ == "__main__":
    register()