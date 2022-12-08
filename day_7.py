from utils import read_input
from dataclasses import dataclass, field
from typing import Optional, Self, Union

inpt = read_input("7")

@dataclass
class File:
    name: str
    file_size: int

    def __repr__(self):
        return f"{self.name} ({self.file_size} byte)"

@dataclass
class Directory:
    name: str
    parent_dir: Optional[Self]
    children: dict[str, Union[Self, File]] = field(default_factory=dict)

    def add_children(self, children: list[Union[File, Self]]) -> None:
        for item in children:
            self.children[item.name] = item

    def calc_file_size(self) -> int:
        file_size = 0
        for item in self.children.values():
            if type(item) == File:
                file_size += item.file_size
            elif type(item) == Directory:
                file_size += item.calc_file_size()

        return file_size

    def __repr__(self):
        if self.parent_dir:
            return f"{self.parent_dir.__str__()}/{self.name}"
        else:
            return f"{self.name}"

root_dir = Directory(name="/root", parent_dir=None)
current_dir = root_dir

idx = 1

while idx < len(inpt):

    command = inpt[idx]

    if "cd" in command:
        #Change to children directory
        dir_name = command.split("cd ")[-1]
        if dir_name == "..":
            current_dir = current_dir.parent_dir
        else:
            current_dir: Directory = current_dir.children[dir_name]
    elif "ls" in command:
        #Add children directories
        results = []
        while (idx + 1 < len(inpt)) and (not inpt[idx + 1].startswith("$")):
            idx += 1
            file = inpt[idx]
            if file.startswith("dir"):
                result = Directory(name=file.split(" ")[-1], parent_dir=current_dir)
            else:
                result = File(name=file.split(" ")[-1], file_size = int(file.split(" ")[0]))
            results.append(result)

        if results:
            current_dir.add_children(results)

    idx += 1


def get_first_solution():

    def add_dir_size(directory: Directory, size_threshold: int) -> int:
        size = 0
        for item in directory.children.values():
            if type(item) == Directory:
                if (file_size := item.calc_file_size()) <= size_threshold:
                    size += file_size
                size += add_dir_size(item, size_threshold)

        return size

    return add_dir_size(root_dir, size_threshold=100000)

def get_second_solution():
    total_used_size = root_dir.calc_file_size()
    total_unused_size = 70000000 - total_used_size
    required_file_size = 30000000
    size_needed = required_file_size - total_unused_size

    def find_all_dir_sizes(directory: Directory) -> list[tuple[str, int]]:
        result = []
        for item in directory.children.values():
            if type(item) == Directory:
                result += [(item.__repr__(), item.calc_file_size())]
                if children_dir_sizes := find_all_dir_sizes(item):
                    result += children_dir_sizes

        return result

    dir_sizes_sorted = sorted(find_all_dir_sizes(root_dir), key= lambda x: x[1])

    return [directory for directory in dir_sizes_sorted if directory[1] >= size_needed][0][1]



print(get_first_solution())
print(get_second_solution())