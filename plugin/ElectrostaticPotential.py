import nanome
from nanome.util import async_callback, Logs
from nanome.util.enums import Integrations, NotificationTypes, VolumeVisualStyle
from nanome.api.volumetric.models import VolumeLayer, VolumeProperties

from . import process, __version__


class ElectrostaticPotential(nanome.AsyncPluginInstance):

    def start(self):
        self.integration.calculate_esp = self.on_integration_request

    @async_callback
    async def on_integration_request(self, request):
        comp_list = request.get_args()
        if not self.validate_comp_is_protein(comp_list):
            error_msg = 'Selected complex must contain a protein'
            self.send_notification(NotificationTypes.error, error_msg)
            Logs.warning(error_msg)
            return
        await self.run_process_and_upload_volume(comp_list)

    @async_callback
    async def on_run(self):
        self.set_plugin_list_button(self.PluginListButtonType.run, "Running...", False)
        complex_list = await self.request_complex_list()
        valid_selection = True
        error_msg = ''
        selected = [c.index for c in complex_list if c.get_selected()]
        if not len(selected) == 1:
            if not selected:
                error_msg = 'Please select a complex.'
            else:
                error_msg = 'Please select only one complex'
            valid_selection = False

        # Only request complex data if valid selection was made
        if valid_selection:
            selected_comps = await self.request_complexes(selected)
            if not self.validate_comp_is_protein(selected_comps):
                error_msg = 'Selected complex must contain a protein'
                valid_selection = False

        if not valid_selection:
            self.send_notification(NotificationTypes.error, error_msg)
            self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)
            return

        await self.run_process_and_upload_volume(selected_comps)

    def validate_comp_is_protein(self, comp_list):
        """Make sure selected complex contains a protein."""
        valid = True
        for comp in comp_list:
            # atoms that are not hetatoms are considered a protein
            protein_found = any(a.is_het is False for a in comp.atoms)
            if not protein_found:
                valid = False
                break
        return valid

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
        properties = VolumeProperties()
        properties._boxed = False
        properties._style = VolumeVisualStyle.SmoothSurface
        properties._use_map_mover = False
        properties._visible = False
        layer0 = VolumeLayer()
        layer0._rmsd = -1
        layer0._color.set_color_rgb(0xDC, 0x14, 0x3C, 0xBE)
        layer1 = VolumeLayer()
        layer1._rmsd = 1
        layer1._color.set_color_rgb(0x2E, 0x37, 0xFE, 0xBE)
        properties._layers = [layer0, layer1]
        self.add_volume(esp_complex, esp_map, properties, comp.index)


def main():
    plugin_name = 'Electrostatic Potential'
    description = 'Calculates Electrostatic Potential Map'
    tags = 'ESP'
    has_advanced_menu = False
    plugin = nanome.Plugin(
        plugin_name, description, tags, has_advanced_menu,
        integrations=[Integrations.calculate_esp],
        version=__version__)
    plugin.set_plugin_class(ElectrostaticPotential)
    plugin.run()


if __name__ == '__main__':
    main()
