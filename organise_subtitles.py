import os
import shutil

SUBTITLES_FOLDER = './subtitles'
FOLDER_STRUCTURE_DEPTH = 3

for filename in os.listdir(SUBTITLES_FOLDER):
    if filename.endswith(".srt"):
        sub_path = SUBTITLES_FOLDER

        # Make folder structure 3 levels deep:
        for i in range(2, 2 + FOLDER_STRUCTURE_DEPTH):
            sub_path = os.path.join(sub_path, filename[i])
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)

        # Now, sub_path points to the directory where the subtitles file should be copied to. Let's copy it
        shutil.copy(os.path.join(SUBTITLES_FOLDER, filename), sub_path)
