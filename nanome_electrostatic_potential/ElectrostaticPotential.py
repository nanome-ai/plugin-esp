import nanome
from nanome.util import Logs
from nanome.util.enums import NotificationTypes, VolumeVisualStyle
from nanome.api.structure import Complex
from nanome._internal._volumetric._volume_layer import _VolumeLayer
from nanome._internal._volumetric._volume_properties import _VolumeProperties
from . import esp_config, _process


class ElectrostaticPotential(nanome.PluginInstance):
    def start(self):
        self.__process = _process.Process(self)
        self.integration.calculate_esp = self.on_integration_request

    def on_integration_request(self, request):
        self.on_receive_target_list(request.get_args())

    def on_run(self):
        self.set_plugin_list_button(self.PluginListButtonType.run, "Running...", False)
        self.request_complex_list(self.on_receive_complex_list)

    def on_receive_complex_list(self, complex_list):
        selected = [c.index for c in complex_list if c.get_selected()]
        if not selected:
            self.send_notification(
                NotificationTypes.error, "Please select a complex")
            return
        if len(selected) > 1:
            self.send_notification(
                NotificationTypes.error, "Please select only one complex")
            return
        self.request_complexes(selected, self.on_receive_target_list)

    def on_receive_target_list(self, target_list):
        target = target_list[0]
        result = self.__process.run(target)
        if result:
            self.upload_esp(target, result)
        self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)

    def upload_esp(self, target, result):
        esp_complex, esp_map = result
        esp_map._name = target.name + '_ESP'
        properties = _VolumeProperties()
        properties._boxed = False
        properties._style = VolumeVisualStyle.SmoothSurface
        properties._use_map_mover = False
        properties._visible = False
        layer0 = _VolumeLayer()
        layer0._rmsd = -1
        layer0._color.set_color_rgb(0xDC, 0x14, 0x3C, 0xBE)
        layer1 = _VolumeLayer()
        layer1._rmsd = 1
        layer1._color.set_color_rgb(0x2E, 0x37, 0xFE, 0xBE)
        properties._layers = [layer0, layer1]
        self.add_volume(esp_complex, esp_map, properties, target.index)


def main():
    plugin = nanome.Plugin('Electrostatic Potential',
                           'Calculates Electrostatic Potential Map', 'ESP', False)
    plugin.set_plugin_class(ElectrostaticPotential)
    plugin.run()


if __name__ == '__main__':
    main()
