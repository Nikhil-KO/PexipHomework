import os
import pathlib

class Observer:

	# Given a path and functions to call in the case of events set up the observer
	def __init__(self, root_path : pathlib.Path, on_modify, on_move, on_create, on_delete) -> None:
		self.root_path = root_path
		self.folder_details = {}
		self.file_details = {}

		# init observered folder
		for path, _, files in os.walk(root_path):
			folder_stats = os.stat(path)
			self.folder_details[folder_stats.st_ino] = [folder_stats, pathlib.Path(path).relative_to(root_path)]
			for file in files:
				file_path = pathlib.Path(os.path.join(path, file))
				stats = os.stat(file_path)
				self.file_details[stats.st_ino] = [stats, file_path.relative_to(root_path)]

		# link functions
		self.on_modify = on_modify
		self.on_move = on_move
		self.on_create = on_create
		self.on_delete = on_delete

	# Check given folder for change
	def check_folder(self, path : str, active_folders : list):
		new_path = pathlib.Path(path).relative_to(self.root_path)
		folder_stats = os.stat(path)
		active_folders.append(folder_stats.st_ino)
		# new folder
		if folder_stats.st_ino not in self.folder_details:
			self.folder_details[folder_stats.st_ino] = [folder_stats, new_path]
			self.on_create(str(new_path), True)
			return
		# folder moved
		old_path = self.folder_details[folder_stats.st_ino][1]
		if old_path != new_path:
			self.folder_details[folder_stats.st_ino][1] = new_path
			self.on_move(old_path, new_path)
		
	# check given file for change
	def check_file(self, path : str, file : str, active_files : list):
		file_path = pathlib.Path(os.path.join(path, file))
		new_stats = os.stat(file_path)
		active_files.append(new_stats.st_ino)
		new_path = file_path.relative_to(self.root_path)
		# new file
		if new_stats.st_ino not in self.file_details:
			self.file_details[new_stats.st_ino] = [new_stats, new_path]
			self.on_create(new_path, False)
			return
		old_file_details = self.file_details[new_stats.st_ino]
		# file renamed/moved
		if old_file_details[1] != new_path:
			old_path = old_file_details[1]
			self.file_details[new_stats.st_ino][1] = new_path
			self.on_move(old_path, new_path)
		# file modifed
		if old_file_details[0].st_mtime != new_stats.st_mtime:
			self.file_details[new_stats.st_ino][0] = new_stats
			self.on_modify(str(new_path))

	def watch(self):
		active_folders = []
		active_files = []
		for path, _, files in os.walk(self.root_path):
			self.check_folder(path, active_folders)
			for file in files:
				try:
					self.check_file(path, file, active_files)
				except FileNotFoundError:
					# FIXME this needs to be reviewed
					pass # file moved or deleted during pass
		# check for deleted folders/files
		deleted_folder = set(self.folder_details.keys()) - set(active_folders)
		deleted_files = set(self.file_details.keys()) -  set(active_files)
		for f in deleted_folder:
			self.on_delete(self.folder_details[f][1], True)
			del self.folder_details[f]
		for f in deleted_files:
			self.on_delete(self.file_details[f][1], False)
			del self.file_details[f]