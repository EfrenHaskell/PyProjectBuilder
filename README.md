# PyProjectBuilder
## Functionality
PyProjectBuilder is a DevTool for setting up Python projects.
A project's file structure can be detailed in a pyspec file.
A pyspec file is divided into different contexts. If no context is specified the filesystem context is used by default.
Users can include any of the following specifications to include in their projects:

 - Git
	- Initialize a Git repo
	- Specify any branches to be created retroactively
 - Installing packages
	- Specify any necessary dependencies -- installs and creates requirements file
 - Module-level dunders
	- Add module-level dunders to python files
	- Dynamically update dunder values
## pyspec
Creating a pyspec file
## Parsing order
Context specifications are parsed in the following order <br>
1. ML Dunders
2. Package installations
3. File structure specifications
4. Git initializations

