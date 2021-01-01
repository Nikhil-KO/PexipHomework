import os
import time
import pathlib

class Observer:

	def __init__(self, root_path : pathlib.Path, folder_details : dict, file_details : dict,
					on_modify, on_move, on_create, on_delete) -> None:
		self.root_path = root_path
		self.folder_details = folder_details
		self.file_details = file_details
		self.on_modify = on_modify
		self.on_move = on_move
		self.on_create = on_create
		self.on_delete = on_delete

	def check_folder(self, path : str, active_folders : list):
		new_path = pathlib.Path(path).relative_to(self.root_path)
		folder_stats = os.stat(path)
		active_folders.append(folder_stats.st_ino)
		# new folder
		if folder_stats.st_ino not in self.folder_details:
			self.folder_details[folder_stats.st_ino] = [folder_stats, new_path]
			self.on_create("directory " + str(new_path))
			return
		# folder moved
		old_path = self.folder_details[folder_stats.st_ino][1]
		if old_path != new_path:
			self.folder_details[folder_stats.st_ino][1] = new_path
			self.on_move("directory from " + str(old_path) + " to " + str(new_path))
		
	def check_file(self, path : str, file : str, active_files : list):
		file_path = pathlib.Path(os.path.join(path, file))
		new_stats = os.stat(file_path)
		active_files.append(new_stats.st_ino)
		new_path = file_path.relative_to(self.root_path)
		# new file
		if new_stats.st_ino not in self.file_details:
			self.file_details[new_stats.st_ino] = [new_stats, new_path]
			self.on_create("file " + str(new_path))
			return
		old_file_details = self.file_details[new_stats.st_ino]
		# file renamed/moved
		if old_file_details[1] != new_path:
			msg = "moved from " + str(old_file_details[1]) + " to " + str(new_path)
			self.file_details[new_stats.st_ino][1] = new_path
			self.on_move(msg)
		# file modifed
		if old_file_details[0].st_mtime != new_stats.st_mtime:
			self.file_details[new_stats.st_ino][0] = new_stats
			self.on_modify(str(new_path))

	def watch(self):
		print("watching folder")
		active_folders = []
		active_files = []
		for path, _, files in os.walk(self.root_path):
			self.check_folder(path, active_folders)
			for file in files:
				self.check_file(path, file, active_files)
