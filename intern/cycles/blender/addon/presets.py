#
# Copyright 2011-2013 Blender Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# <pep8 compliant>

from bl_operators.presets import AddPresetBase
from bpy.types import Operator


class AddPresetIntegrator(AddPresetBase, Operator):
    '''Add an Integrator Preset'''
    bl_idname = "render.cycles_integrator_preset_add"
    bl_label = "Add Integrator Preset"
    preset_menu = "CYCLES_MT_integrator_presets"

    preset_defines = [
        "cycles = bpy.context.scene.cycles"
    ]

    preset_values = [
        "cycles.max_bounces",
        "cycles.diffuse_bounces",
        "cycles.glossy_bounces",
        "cycles.transmission_bounces",
        "cycles.volume_bounces",
        "cycles.transparent_max_bounces",
        "cycles.caustics_reflective",
        "cycles.caustics_refractive",
        "cycles.blur_glossy"
    ]

    preset_subdir = "cycles/integrator"


class AddPresetSampling(AddPresetBase, Operator):
    '''Add a Sampling Preset'''
    bl_idname = "render.cycles_sampling_preset_add"
    bl_label = "Add Sampling Preset"
    preset_menu = "CYCLES_MT_sampling_presets"

    preset_defines = [
        "cycles = bpy.context.scene.cycles"
    ]

    preset_values = [
        "cycles.samples",
        "cycles.preview_samples",
        "cycles.aa_samples",
        "cycles.preview_aa_samples",
        "cycles.diffuse_samples",
        "cycles.glossy_samples",
        "cycles.transmission_samples",
        "cycles.ao_samples",
        "cycles.mesh_light_samples",
        "cycles.subsurface_samples",
        "cycles.volume_samples",
        "cycles.use_square_samples",
        "cycles.progressive",
        "cycles.seed",
        "cycles.sample_clamp_direct",
        "cycles.sample_clamp_indirect",
        "cycles.sample_all_lights_direct",
        "cycles.sample_all_lights_indirect",
    ]

    preset_subdir = "cycles/sampling"

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

classes = (
    AddPresetIntegrator,
    AddPresetSampling,
    AddPresetBcd,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
