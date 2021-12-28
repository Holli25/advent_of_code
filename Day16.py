from typing import List, Tuple, Dict

HEX = {"0":"0000", "1":"0001", "2":"0010", "3":"0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111", "8":"1000", "9":"1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E":"1110", "F":"1111"}

def read_data(testing: bool = False) -> Tuple[List[int], int]:
    if testing:
        filename = "Test_inputs/Day16.txt"
    else:
        filename = "Inputs/Day16.txt"

    with open(filename) as file:
        return file.read().strip()

class Decryption():
    def __init__(self, input):
        self.binary = self.convert_to_binary(input)
        self.sums_of_versions = 0

    def convert_to_binary(self, input: str) -> str:
        return "".join([HEX[i] for i in input])

    def get_version(self, input: str) -> int:
        return int(input[:3], 2)

    def get_type_id(self, input: str) -> int:
        return int(input[3:6], 2)

    def get_literal(self, input: str) -> Tuple[str, int]:
        relevant_part: str = input[6:]
        output: List[str] = []
        for index, start_number in enumerate(relevant_part[::5]):
            real_index = index * 5 + 1
            if int(start_number) == 1:
                output.append(relevant_part[real_index:real_index+4])
            elif int(start_number) == 0:
                output.append(relevant_part[real_index:real_index+4])
                break
        output = "".join(output)
        return input[6 + real_index + 4:], int(output, 2) # 6 from removed part, real_index on top and 4 for last bit that was read

    def get_length_type_0(self, input: str, type_id: int) -> Tuple[str, int]:
        next_packages_length = int(input[:15], 2)
        # print(f"Next length is: {next_packages_length}")
        packages = input[15:15 + next_packages_length]
        packet_value = 0
        index = 0
        while packages:
            packages, value = self.do_one_package(packages)
            packet_value = self.get_new_packet_value(packet_value, value, type_id, index)
            index += 1
            # print(f"Literal called from get_length_type_0 id {number}")
        # print(packet_value)
        return input[15 + next_packages_length:], packet_value

    def get_length_type_1(self, input: str, type_id:int) -> str:
        number_of_sub_packages = int(input[:11], 2)
        packet_value = 0
        # print(f"Expecting {number_of_sub_packages} packages")
        remaining_input = input[11:]
        for package in range(number_of_sub_packages):
            remaining_input, value = self.do_one_package(remaining_input)
            packet_value = self.get_new_packet_value(packet_value, value, type_id, package)
            # print(f"Literal called from get_length_type_1 is {number}")
        # print(packet_value)
        return remaining_input, packet_value

    def get_new_packet_value(self, packet_value: int, value: int, type_id: int, packet_number: int) -> int:
        # print(f"Original packet_value: {packet_value}.\n New packet value: {value}.\n Type_id: {type_id}.\n")
        if type_id == 0:
            return packet_value + value
        elif type_id == 1:
            if packet_number == 0:
                return value
            return packet_value * value
        elif type_id == 2:
            if packet_number == 0:
                return value
            return min(packet_value, value)
        elif type_id == 3:
            return max(packet_value, value)
        elif type_id == 5:
            if packet_number != 0:
                return int(packet_value > value)
            else:
                return value
        elif type_id == 6:
            if packet_number != 0:
                return int(packet_value < value)
            else:
                return value
        elif type_id == 7:
            if packet_number != 0:
                return int(packet_value == value)
            else:
                return value

    def do_full_package(self):
        return self.do_one_package(self.binary)


    def do_one_package(self, input:str):
        version = self.get_version(input)
        self.sums_of_versions += version
        # print(f"Version is: {version}, the sum is {self.sums_of_versions}")
        type_id = self.get_type_id(input)

        if type_id == 4:
            return self.get_literal(input)
        length_type_id = int(input[6])
        if length_type_id == 0:
            # print(f"Found operator with length type 0")
            return self.get_length_type_0(input[7:], type_id)
        elif length_type_id == 1:
            # print(f"Found operator with length type 1")
            return self.get_length_type_1(input[7:], type_id)


def part_one() -> int:
    input = read_data(False)
    decrypter = Decryption(input)
    decrypter.do_full_package()
    return decrypter.sums_of_versions

def part_two() -> int:
    input = read_data()
    decrypter = Decryption(input)
    return decrypter.do_full_package()[1]

print(part_one())
print(part_two())
