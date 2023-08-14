from datetime import datetime

from pyfileflow import FileOrganizer, Path, Rule

# Initialize the FileOrganizer
organizer = FileOrganizer("/path/to/source_folder")


# Define a rule to move files with a certain file size to a different folder
def file_size_condition(path: Path):
    return path.stat().st_size > 1024  # Example: Move files larger than 1 KB


move_large_files_rule = Rule(
    action="move",
    condition=file_size_condition,
    destination_folder="/path/to/large_files/",
)

# Add the rule to the organizer
organizer.add_rule(move_large_files_rule)


# Define a rule to sort files by creation date into yearly folders
def creation_year_condition(path: Path):
    path.time_created: datetime
    return path.time_created.year


sort_by_year_rule = Rule(
    action="move_by_value",
    value=creation_year_condition,
    destination_template="/path/to/yearly_folders/{}/",
    step=1,  # One folder per year
)

# Add the rule to the organizer
organizer.add_rule(sort_by_year_rule)

# Apply the rules to the files in the source folder
organizer.apply_rules()
