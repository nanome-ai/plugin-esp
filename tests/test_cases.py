import asyncio
import os
import unittest
from unittest.mock import patch
from random import randint

from unittest.mock import MagicMock
from nanome.api.structure import Chain, Complex, Molecule, Workspace
from nanome.util.stream import StreamCreationError
from nanome_electrostatic_potential.ElectrostaticPotential import ElectrostaticPotential


fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def run_awaitable(awaitable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(awaitable(*args, **kwargs))
    loop.close()


class ESPTestCase(unittest.TestCase):
    """Test different combinations of args for calculate_interactions."""

    def setUp(self):
        tyl_pdb = f'{fixtures_dir}/5ceo.pdb'
        self.complex = Complex.io.from_pdb(path=tyl_pdb)
        self.workspace = Workspace()
        for atom in self.complex.atoms:
            atom.index = randint(1000000000, 9999999999)

        self.plugin_instance = ElectrostaticPotential()
        self.plugin_instance._run_text = 'running'
        self.plugin_instance._run_usable = True
        self.plugin_instance._advanced_settings_text = "Advanced Settings"
        self.plugin_instance._advanced_settings_usable = True
        self.plugin_instance._custom_data = ()
        self.plugin_instance._permissions = {}

        self.plugin_instance.start()
        self.plugin_instance._network = MagicMock()

        # Select ligand atoms
        # target_complex = self.complex
        # chain_name = 'HC'
        # chain = next(ch for ch in target_complex.chains if ch.name == chain_name)
        # for atom in chain.atoms:
        #     atom.selected = True


    @patch('nanome.api.plugin_instance.PluginInstance.request_complexes')
    @patch('nanome.api.plugin_instance.PluginInstance.request_complex_list')
    def test_run(self, request_complex_list_mock, request_complexes_mock, *mocks):
        """Validate calculate_interactions call where ligand is on a separate complex."""
        # Set up mocked result for create_writing_stream_mock
        self.complex._selected = True
        request_list_fut = asyncio.Future()
        request_list_fut.set_result([self.complex])
        request_complex_list_mock.return_value = request_list_fut

        deep_fut = asyncio.Future()
        deep_fut.set_result([self.complex])
        request_complexes_mock.return_value = deep_fut

        return run_awaitable(self.validate_esp_run)

    async def validate_esp_run(self):
        """Run plugin.calculate_interactions with provided args and make sure lines are added to LineManager."""
        self.plugin_instance._network = MagicMock()
        await self.plugin_instance.on_run()
