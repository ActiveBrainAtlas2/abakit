import os
from abakit.settings import DATA_PATH


class FileLocationManager(object):
    """Create a class for processing the pipeline,"""

    def __init__(self, stack, DATA_PATH=DATA_PATH):
        """setup the directory, file locations
        Args:
            stack: the animal brain name, AKA prep_id
        """
        self.animal = stack
        self.root = os.path.join(DATA_PATH, "pipeline_data")
        self.stack = os.path.join(self.root, stack)
        self.prep = os.path.join(self.stack, "preps")
        self.czi = os.path.join(self.stack, "czi")
        self.tif = os.path.join(self.stack, "tif")
        self.thumbnail_original = os.path.join(self.stack, "thumbnail_original")
        self.jp2 = os.path.join(self.stack, "jp2")
        self.thumbnail = os.path.join(self.prep, "CH1", "thumbnail")
        self.histogram = os.path.join(self.stack, "histogram")
        self.thumbnail_web = os.path.join(self.stack, "www", "scene")
        self.neuroglancer_data = os.path.join(self.stack, "neuroglancer_data")
        self.brain_info = os.path.join(self.stack, "brains_info")
        self.operation_configs = os.path.join(
            self.brain_info, "operation_configs"
        )
        self.mxnet_models = os.path.join(self.brain_info, "mxnet_models")
        self.atlas_volume = os.path.join(
            self.brain_info, "CSHL_volumes", "atlasV7", "score_volumes"
        )
        self.classifiers = os.path.join(self.brain_info, "classifiers")
        self.custom_transform = os.path.join(
            self.brain_info, "custom_transform"
        )
        self.mouseatlas_tmp = os.path.join(self.brain_info, "mouseatlas_tmp")
        self.elastix_dir = os.path.join(self.prep, "elastix")
        self.full_masked = os.path.join(self.prep, "full_masked")
        self.full_aligned = os.path.join(self.prep, "full_aligned")
        self.masks = os.path.join(self.prep, "masks")
        self.thumbnail_masked = os.path.join(self.masks, "thumbnail_masked")
        self.thumbnail_colored = os.path.join(self.masks, "thumbnail_colored")
        self.rotated_and_padded_thumbnail_mask = os.path.join(
            self.masks, "thumbnail_rotated_and_padded"
        )
        self.aligned_rotated_and_padded_thumbnail_mask = os.path.join(
            self.masks, "thumbnail_aligned_rotated_and_padded"
        )
        self.shell = os.path.join(self.stack, "shell")
        self.segmentation_layer = os.path.join(self.root, "structures")

    def get_full(self, channel=1):
        """returns the directory to the full resolution tiff files

        Args:
            channel (int, optional): channel number for which the files are considered. Defaults to 1.

        Returns:
            str: path to the full size tiff folder
        """
        return os.path.join(self.prep, f"CH{channel}", "full")

    def get_thumbnail(self, channel=1):
        """returns the path to the downsampeld tiff files

        Args:
            channel (int, optional): The channel in question. Defaults to 1.

        Returns:
            str: path to the downsampled tiff files
        """
        return os.path.join(self.prep, f"CH{channel}", "thumbnail")

    def get_elastix(self, channel=1):
        """get the path to files storing the elastixs transformation.  This is likely depricated

        Args:
            channel (int, optional): channel in question. Defaults to 1.

        Returns:
            str: path to the elastix file
        """
        return os.path.join(self.prep, f"CH{channel}", "elastix")

    def get_full_cleaned(self, channel=1):
        """get the full resolution tiff files where the debrie around the tissue has been cleaned

        Args:
            channel (int, optional): the channel in question. Defaults to 1.

        Returns:
            str: the path to full sized cleaned images
        """
        return os.path.join(self.prep, f"CH{channel}", "full_cleaned")

    def get_full_aligned(self, channel=1):
        """Get path to full resolution images after within stack alignment

        Args:
            channel (int, optional): channel number. Defaults to 1.

        Returns:
            str: path to the full resolution within stack aligned images
        """
        return os.path.join(self.prep, f"CH{channel}", "full_aligned")

    def get_thumbnail_aligned(self, channel=1):
        """get downsampled aligned images

        Args:
            channel (int, optional): channel number. Defaults to 1.

        Returns:
            str: path to downsampled aligned images
        """
        return os.path.join(self.prep, f"CH{channel}", "thumbnail_aligned")

    def get_thumbnail_cleaned(self, channel=1):
        """get path to downsampled cleaned images

        Args:
            channel (int, optional): channel number . Defaults to 1.

        Returns:
            str: path to downsampled cleaned images
        """
        return os.path.join(self.prep, f"CH{channel}", "thumbnail_cleaned")

    def get_normalized(self, channel=1):
        """get path to normalized images

        Args:
            channel (int, optional): channel number. Defaults to 1.

        Returns:
            str: path to normalized images
        """
        return os.path.join(self.prep, f"CH{channel}", "normalized")

    def get_histogram(self, channel=1):
        """get the histogram of pixel intensity for the images

        Args:
            channel (int, optional): channel number. Defaults to 1.

        Returns:
            str: file path
        """
        return os.path.join(self.histogram, f"CH{channel}")

    def get_neuroglancer(self, downsample=True, channel=1, rechunck=False):
        """get path to cloud volume neuroglancer neuroglancer image layer files

        Args:
            downsample (bool, optional): if the neuroglancer cloud volume is for downsampled image. Defaults to True.
            channel (int, optional): channel number. Defaults to 1.
            rechunck (bool, optional): whether rechunking is performed. Defaults to False.

        Returns:
            str: path of the cloudvolume neuroglancer image layer
        """
        if downsample:
            channel_outdir = f"C{channel}T"
        else:
            channel_outdir = f"C{channel}"
        if not rechunck:
            channel_outdir += "_rechunkme"
        return os.path.join(self.neuroglancer_data, f"{channel_outdir}")

    def get_logdir(self):
        """returns the directory for log files (must be rw)

        Returns:
            str: path to the log dir and file [for pipeline]
        """
        return os.path.join(self.stack, "pipeline_" + self.animal + ".log")
