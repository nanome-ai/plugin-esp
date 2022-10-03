import nanome
from nanome.util import async_callback
from nanome.util.enums import Integrations, NotificationTypes, VolumeVisualStyle
from nanome._internal._volumetric._volume_layer import _VolumeLayer
from nanome._internal._volumetric._volume_properties import _VolumeProperties
from . import process


class ElectrostaticPotential(nanome.AsyncPluginInstance):

    def start(self):
        self.integration.calculate_esp = self.on_integration_request

    @async_callback
    async def on_integration_request(self, request):
        await self.run_process_and_upload_volume(request.get_args())

    @async_callback
    async def on_run(self):
        self.set_plugin_list_button(self.PluginListButtonType.run, "Running...", False)
        complex_list = await self.request_complex_list()
        selected = [c.index for c in complex_list if c.get_selected()]
        if not selected:
            self.send_notification(
                NotificationTypes.error, "Please select a complex")
            self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)
            return
        if len(selected) > 1:
            self.send_notification(
                NotificationTypes.error, "Please select only one complex")
            self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)
            return
        selected_comps = await self.request_complexes(selected)
        await self.run_process_and_upload_volume(selected_comps)

    async def run_process_and_upload_volume(self, comp_list):
        target = comp_list[0]
        proc = process.ESPProcess(self)
        result = await proc.run(target)
        if result:
            self.upload_esp(target, result)
        self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)

    def upload_esp(self, comp, result):
        esp_complex, esp_map = result
        esp_map._name = comp.name + '_ESP'
        properties = _VolumeProperties()
        properties._boxed = False
        properties._style = VolumeVisualStyle.Mesh
        properties._use_map_mover = False
        properties._visible = False
        layer0 = _VolumeLayer()
        layer0._rmsd = -1
        layer0._color.set_color_rgb(0xDC, 0x14, 0x3C, 0xBE)
        layer1 = _VolumeLayer()
        layer1._rmsd = 1
        layer1._color.set_color_rgb(0x2E, 0x37, 0xFE, 0xBE)
        properties._layers = [layer0, layer1]
        self.add_volume(esp_complex, esp_map, properties, comp.index)


def main():
    plugin = nanome.Plugin('Electrostatic Potential', 'Calculates Electrostatic Potential Map', 'ESP', False, integrations=[Integrations.calculate_esp])
    plugin.set_plugin_class(ElectrostaticPotential)
    plugin.run()


if __name__ == '__main__':
    main()
