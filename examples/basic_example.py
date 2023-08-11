import pyfileflow as pff

pff.add_rule(
    Rule(
        conditions=[lambda file: file.size > 0, ...],
        folders=["path/to/sorted", "path2/to/sorted2"],
    )
)

pff.sort_folder("path/to/sort")
