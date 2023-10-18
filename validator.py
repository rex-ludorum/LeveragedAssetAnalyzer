import os

allDirsAndFiles = []
startDate = "2021-03-20"
dirList = os.listdir()
dirList = [dir for dir in dirList if os.path.isdir(dir) and dir != ".git"]
for dir in dirList:
	tempDir = []
	tempDir.append(dir)
	files = os.listdir(dir)
	startIndex = next(x for x, val in enumerate(files) if val >= startDate)
	files = files[startIndex:]
	tempDir += files
	allDirsAndFiles.append(tempDir)

# make sure we have downloaded data consistently across all assets
for list in allDirsAndFiles[1:]:
	if allDirsAndFiles[0][1:] != list[1:]:
		print(allDirsAndFiles[0][0] + " has a discrepancy with " + list[0])
