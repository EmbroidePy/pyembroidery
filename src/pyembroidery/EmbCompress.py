def expand(data, uncompressed_size=None):
    emb_compress = EmbCompress()
    return emb_compress.decompress(data, uncompressed_size)


def compress(data):
    size = len(data)
    return (
        bytearray([(size >> 0) & 0xFF, (size >> 8) & 0xFF, 0x02, 0xA0, 0x01, 0xFE])
        + data
    )


class Huffman:
    def __init__(self, lengths=None, value=0):
        self.default_value = value
        self.lengths = lengths
        self.table = None
        self.table_width = 0

    def build_table(self):
        """Build an index huffman table based on the lengths. lowest index value wins in a tie."""
        self.table_width = max(self.lengths)
        self.table = []
        size = 1 << self.table_width
        for bit_length in range(1, self.table_width + 1):
            size /= 2.0
            for len_index in range(0, len(self.lengths)):
                length = self.lengths[len_index]
                if length == bit_length:
                    self.table += [len_index] * int(size)

    def lookup(self, byte_lookup):
        """lookup into the index, returns value and length
        must be requested with 2 bytes."""
        if self.table is None:
            return self.default_value, 0
        v = self.table[byte_lookup >> (16 - self.table_width)]
        return v, self.lengths[v]


class EmbCompress:
    def __init__(self):
        self.bit_position = 0
        self.input_data = None
        self.block_elements = None
        self.character_huffman = None
        self.distance_huffman = None

    def get_bits(self, start_pos_in_bits, length):
        end_pos_in_bits = start_pos_in_bits + length - 1
        start_pos_in_bytes = int(start_pos_in_bits / 8)
        end_pos_in_bytes = int(end_pos_in_bits / 8)
        value = 0
        for i in range(start_pos_in_bytes, end_pos_in_bytes + 1):
            value <<= 8
            try:
                value |= self.input_data[i] & 0xFF
            except IndexError:
                pass
        unused_bits_right_of_sample = (8 - (end_pos_in_bits + 1) % 8) % 8
        mask_sample_bits = (1 << length) - 1
        original = (value >> unused_bits_right_of_sample) & mask_sample_bits
        return original

    def pop(self, bit_count):
        value = self.peek(bit_count)
        self.slide(bit_count)
        return value

    def peek(self, bit_count):
        return self.get_bits(self.bit_position, bit_count)

    def slide(self, bit_count):
        self.bit_position += bit_count

    def read_variable_length(self):
        m = self.pop(3)
        if m != 7:
            return m
        for q in range(
            0, 13
        ):  # max read is 16 bit, 3 bits already used. It can't exceed 16-3
            s = self.pop(1)
            if s == 1:
                m += 1
            else:
                break
        return m

    def load_character_length_huffman(self):
        count = self.pop(5)
        if count == 0:
            v = self.pop(5)
            huffman = Huffman(value=v)
        else:
            huffman_code_lengths = [0] * count
            index = 0
            while index < count:
                if index == 3:  # Special index 3, skip up to 3 elements.
                    index += self.pop(2)
                huffman_code_lengths[index] = self.read_variable_length()
                index += 1
            huffman = Huffman(huffman_code_lengths, 8)
            huffman.build_table()
        return huffman

    def load_character_huffman(self, length_huffman):
        count = self.pop(9)
        if count == 0:
            v = self.pop(9)
            huffman = Huffman(value=v)
        else:
            huffman_code_lengths = [0] * count
            index = 0
            while index < count:
                h = length_huffman.lookup(self.peek(16))
                c = h[0]
                self.slide(h[1])
                if c == 0:  # C == 0, skip 1.
                    c = 1
                    index += c
                elif c == 1:  # C == 1, skip 3 + read(4)
                    c = 3 + self.pop(4)
                    index += c
                elif c == 2:  # C == 2, skip 20 + read(9)
                    c = 20 + self.pop(9)
                    index += c
                else:
                    c -= 2
                    huffman_code_lengths[index] = c
                    index += 1
            huffman = Huffman(huffman_code_lengths)
            huffman.build_table()
        return huffman

    def load_distance_huffman(self):
        count = self.pop(5)
        if count == 0:
            v = self.pop(5)
            huffman = Huffman(value=v)
        else:
            index = 0
            lengths = [0] * count
            for i in range(0, count):
                lengths[index] = self.read_variable_length()
                index += 1
            huffman = Huffman(lengths)
            huffman.build_table()
        return huffman

    def load_block(self):
        self.block_elements = self.pop(16)
        character_length_huffman = self.load_character_length_huffman()
        self.character_huffman = self.load_character_huffman(character_length_huffman)
        self.distance_huffman = self.load_distance_huffman()

    def get_token(self):
        if self.block_elements <= 0:
            self.load_block()
        self.block_elements -= 1
        h = self.character_huffman.lookup(self.peek(16))
        self.slide(h[1])
        return h[0]

    def get_position(self):
        h = self.distance_huffman.lookup(self.peek(16))
        self.slide(h[1])
        if h[0] == 0:
            return 0
        v = h[0] - 1
        v = (1 << v) + self.pop(v)
        return v

    def decompress(self, input_data, uncompressed_size=None):
        self.input_data = input_data
        output_data = []
        self.block_elements = -1
        bits_total = len(input_data) * 8
        while bits_total > self.bit_position and (
            uncompressed_size is None or len(output_data) <= uncompressed_size
        ):
            character = self.get_token()
            if character <= 255:  # literal.
                output_data.append(character)
            elif character == 510:
                break  # END
            else:
                length = character - 253  # Min length is 3. 256-253=3.
                back = self.get_position() + 1
                position = len(output_data) - back
                if back > length:
                    # Entire lookback is already within output data.
                    output_data += output_data[position : position + length]
                else:
                    # Will read & write the same data at some point.
                    for i in range(position, position + length):
                        output_data.append(output_data[i])
        return output_data
