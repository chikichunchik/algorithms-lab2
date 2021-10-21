import json


class DB:
    def __init__(self, index_file_path, main_file_path, is_new=False, expected_elements_number=500, block_size=10):
        self.__next_index = 0
        self.index_file_path = index_file_path
        self.main_file_path = main_file_path
        self.__block_size = block_size
        if is_new:
            open(index_file_path, 'w').close()
            open(main_file_path, 'w').close()
            generated_index_file = {}
            generated_main_file = {}
            for i in range(expected_elements_number // block_size):
                generated_index_file[block_size * (i + 1)] = i
                generated_main_file[i] = {}
            with open(index_file_path, 'r+') as index_file, open(main_file_path, 'r+') as main_file:
                json.dump(generated_index_file, index_file)
                json.dump(generated_main_file, main_file)

    def add(self, element):
        block_number = self.__get_block_number(self.__next_index)

        with open(self.main_file_path, 'r') as main_file:
            blocks = json.load(main_file)
            blocks[str(block_number)][self.__next_index] = str(element)

        self.__write_main_file(blocks)

        self.__next_index += 1

    def delete(self, index):
        with open(self.main_file_path, 'r') as main_file:
            blocks = json.load(main_file)
            blocks[str(self.__get_block_number(index))].pop(str(index))
            self.__write_main_file(blocks)

    def set(self, index, element):
        with open(self.main_file_path, 'r') as main_file:
            blocks = json.load(main_file)
            if str(index) not in blocks[str(self.__get_block_number(index))]:
                class NoSuchElement(Exception):
                    pass

                raise NoSuchElement
            blocks[str(self.__get_block_number(index))][str(index)] = str(element)
            self.__write_main_file(blocks)

    def __get_block_number(self, index):
        with open(self.index_file_path, 'r') as index_file:
            indexes = json.load(index_file)
        index_range = list(indexes.keys())[-1] if ((index // self.__block_size) + 1) * self.__block_size >= \
                                                  int(list(indexes.keys())[-1]) else ((index // self.__block_size) + 1) * self.__block_size
        if str(index_range) == '0':
            index_range = indexes.values()[0]
        return indexes[str(index_range)]

    @staticmethod
    def __binary_search(collection, value):
        mid = len(collection) // 2
        low = 0
        high = len(collection) - 1

        while collection[mid] != value and low <= high:
            if value > collection[mid]:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2

        if low > high:
            class NoSuchElement(Exception):
                pass

            raise NoSuchElement
        else:
            return mid

    def __write_main_file(self, content):
        with open(self.main_file_path, 'w+') as main_file:
            json.dump(content, main_file)
