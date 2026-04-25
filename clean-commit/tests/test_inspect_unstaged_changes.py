import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_unstaged_changes.py"
spec = importlib.util.spec_from_file_location("inspect_unstaged_changes", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class InspectUnstagedChangesTests(unittest.TestCase):
    def test_classifies_generated_directory_and_metadata_noise(self):
        labels = module.classify_path_metadata(
            "dist/app.js", Path("/tmp/dist/app.js"), exists=False
        )
        self.assertIn("generated-or-build-artifact", labels)

        labels = module.classify_path_metadata(
            "docs/.DS_Store", Path("/tmp/docs/.DS_Store"), exists=False
        )
        self.assertIn("local-metadata", labels)

    def test_classifies_large_and_binary_files(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            large = tmp_path / "large.log"
            large.write_bytes(b"x" * (module.LARGE_FILE_BYTES + 1))
            labels = module.classify_path_metadata("large.log", large)
            self.assertIn("large-file", labels)

            binary = tmp_path / "image.bin"
            binary.write_bytes(b"abc\0def")
            labels = module.classify_path_metadata("image.bin", binary)
            self.assertIn("binary-or-non-text", labels)


if __name__ == "__main__":
    unittest.main()
