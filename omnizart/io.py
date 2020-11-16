import os
import pickle

import yaml
import librosa
from spleeter.audio.adapter import get_default_audio_adapter

from omnizart.utils import ensure_path_exists


def dump_pickle(data, save_to):
    """Dump data to the given path.

    Parameters
    ----------
    data: python objects
        Data to store. Should be python built-in types like `dict`, `list`, `str`, `int`, etc
    save_to: Path
        The full path to store the pickle file, including file name.
        Will create the directory if the given path doesn't exist.

    """
    base_dir = os.path.dirname(save_to)
    ensure_path_exists(base_dir)
    with open(save_to, "wb") as pkl_file:
        pickle.dump(data, pkl_file)


def load_pickle(pickle_file):
    """Load pickle file from the given path

    Read and returns the data from the given pickle file path

    Parameters
    ----------
    pickle_file: Path
        The full path to the pickle file for read

    Returns
    -------
    object
        Python object, could be `dict`, `list`, `str`, etc.
    """
    return pickle.load(open(pickle_file, "rb"))


def load_audio(audio_path, sampling_rate=44100, mono=True):
    """Load audio with spleeter.

    A much faster and general approach for loading audio comparing to use librosa.
    This function also allows to read .mp3 files.

    Parameters
    ----------
    audio_path: Path
        Path to the audio.
    sampling_rate: int
        Target sampling rate after loaded.
    mono: bool
        Wether to transform the audio into monophonic channel.

    Returns
    -------
    audio: 1D numpy array
        Raw data of the audio.
    fs: int
        Sampling rate of the audio. Will be the same as the given ``sampling_rate``.
    """
    audio_loader = get_default_audio_adapter()
    audio, fs = audio_loader.load(audio_path, sample_rate=sampling_rate)
    if mono:
        audio = librosa.to_mono(audio.T)
    return audio, fs


def load_audio_with_librosa(audio_path, sampling_rate=44100, mono=True):
    """Load audio from the given path with librosa.load

    Parameters
    ----------
    audio_path: Path
        Path to the audio.
    sampling_rate: int
        Target sampling rate after loaded.
    mono: bool
        Wether to transform the audio into monophonic channel.

    Returns
    -------
    audio: 1D numpy array
        Raw data of the audio.
    fs: int
        Sampling rate of the audio. Will be the same as the given ``sampling_rate``.
    """
    return librosa.load(audio_path, mono=mono, sr=sampling_rate)


def load_yaml(yaml_path):
    return yaml.load(open(yaml_path, "r"), Loader=yaml.Loader)


def write_yaml(json_obj, output_path, dump=True):
    # If dump is false, then the json_obj should be yaml string already.
    out_str = yaml.dump(json_obj) if dump else json_obj
    open(output_path, "w").write(out_str)