from abc import ABCMeta, abstractmethod
from scipy.io import wavfile
import numpy as np
import wave


class Compress(metaclass=ABCMeta):
    """ superclass of compress

    Args:
        filename (str): seq of the file we need to compress
    """
    def __init__(self, filename):
        self._filename = filename
        _, sig = wavfile.read('../wav_source/{}.wav'.format(filename))
        self._sig = np.array(sig, dtype=np.int16)

    @abstractmethod
    def compress(self):
        """ compress sig information in specific algorithm and write it into the disk

        """
        pass


class Decompress(metaclass=ABCMeta):
    """ superclass of decompress, write the decompressed file into the disk directly

    Args:
        filename (str): name of the compressed file we need to decompress
        byte (int): 2 -> 8bit, otherwise -> 4bit
    """
    def __init__(self, filename, byte):
        with open(filename+'.dpc', 'rb') as f:
            file = f.read()
            self._head = np.int16((file[0] << 8) + file[1])
            dif = []
            for i, x in enumerate(file):
                if i < 2:
                    continue
                if byte == 2:
                    dif.append(np.int8(x))
                else:
                    dif.append(np.uint8(x) >> 4)
                    dif.append(np.uint8(x) & 0x0f)
            self._dif = np.array(dif, dtype=np.int8)
            self._sig = self.decompress()

        with wave.open('de'+filename+'.pcm', 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(self._sig)

    @abstractmethod
    def decompress(self):
        """ decompress the compressed file information according to the specific algorithm

        :return: decompressed signal information
        """
        pass
