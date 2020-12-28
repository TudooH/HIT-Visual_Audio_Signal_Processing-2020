import numpy as np

from lab5.dpcm import Compress, Decompress


mapping1_dict = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8}
mapping2_dict = {0: 0, 1: 1.5, 2: 3.5, 3: 6.5, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11}


class Compress2(Compress):
    def __init__(self, filename):
        super(Compress2, self).__init__(filename)

    @staticmethod
    def mapping1(x):
        c = mapping1_dict[min(11, round(np.log(abs(x) + 1)))]
        return min(15, 8 + np.sign(x) * c)

    @staticmethod
    def mapping2(x):
        sig = 1 if x >= 8 else -1
        c = (x - 8) * sig
        return (np.exp(mapping2_dict[c]) - 1) * sig

    def compress(self):
        dif = []
        tmp = self._sig[0]
        for i, x in enumerate(self._sig):
            if i == 0:
                continue
            dif.append(self.mapping1(x - tmp))
            tmp = min(32767, max(tmp + self.mapping2(dif[-1]), -32768))

        dif = np.array(dif, dtype=np.uint8)
        with open('compressed2/{}.dpc'.format(self._filename), 'wb') as f:
            f.write(np.uint8(self._sig[0] >> 8))
            f.write(np.uint8(self._sig[0] & 0x00ff))
            for i in range(len(dif)):
                if i % 2 == 0:
                    continue
                f.write(np.uint8((dif[i-1] << 4) + dif[i]))


class Decompress2(Decompress):
    def __init__(self, filename):
        super(Decompress2, self).__init__(filename, 1)

    @staticmethod
    def mapping(x):
        sig = 1 if x >= 8 else -1
        c = (x - 8) * sig
        return (np.exp(mapping2_dict[c]) - 1) * sig

    def decompress(self):
        sig = [self._head]
        for x in self._dif:
            sig.append(min(32767, max(sig[-1] + self.mapping(x), -32768)))

        return np.array(sig, dtype=np.int16)
