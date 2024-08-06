from PIL import Image, ImageFile
from PIL.ExifTags import GPS
import struct
from io import BytesIO
from typing import IO

def _accept(prefix):
    return prefix[:2] == b"CK"


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

class CLKImageFile(ImageFile.ImageFile):

    format = "CLK"
    format_description = "CLK RGB image"

    def _open(self):
        self.fp.seek(2)
        width = int.from_bytes(self.fp.read(2),"little")
        height = int.from_bytes(self.fp.read(2),"little")
        # size in pixels (width, height)
        self._size = (width,height)

        decoder = "CLK"

        self._mode = "RGB"

        self.tile = [(decoder, (0, 0) + self.size, 0, (self.mode, 0, 1))]

class CLKDecoder(ImageFile.PyDecoder):
    _pulls_fd = True
    def decode(self, buffer: bytes)->tuple[int,int]:
        data = bytearray()
        self.fd.seek(2)
        width = int.from_bytes(self.fd.read(2),"little")
        height = int.from_bytes(self.fd.read(2),"little")
        for i in range(width*height):
            try:
                bytes = int.from_bytes(self.fd.read(2),"little")
                r = (0b1111100000000000 & bytes) >> 8
                g = (0b0000011111100000 & bytes) >> 3
                b = (0b0000000000011111 & bytes ) << 3
                data += r.to_bytes()
                data += g.to_bytes()
                data += b.to_bytes()
            except Exception as e:
                print(r,g,b)
                print(e)
        self.set_as_raw(data)
        return -1,0

class CLKEncoder(ImageFile.PyEncoder):
    _pushes_fd = True
    def encode(self, bufsize:int) -> tuple[int, int, bytes]:
        image = self.im
        if image.mode != "RGB":
            image = image.convert("RGB")
        w, h= image.size
        data = bytearray()
        data += bytes((ord('C'),ord('K')))
        data += w.to_bytes(2,"little")
        data += h.to_bytes(2,"little")
        for y in range(h):
            for x in range(w):
                r, g, b = image.getpixel((x, y))
                data += (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)).to_bytes(2,"little")
        return len(data), 0, data

def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    ImageFile._save(im, fp, [("CLK", (0, 0) + im.size, 0, im.mode)])

Image.register_open(CLKImageFile.format, CLKImageFile, _accept)
Image.register_decoder("CLK",CLKDecoder)
Image.register_encoder("CLK",CLKEncoder)
Image.register_save("CLK", _save)
Image.register_extensions(
    CLKImageFile.format,
    [
        ".clk",
    ],
)
