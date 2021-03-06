# Sort files from LOST.DIR

Quick script to sort files found in Android's LOST.DIR directory. This directory is where files recovered during fsck will occasionally wind up.

Currently handles mp3 and mp4 audio files correctly, restoring them to <dest>/mp3/artist/album/track.ext. Other files are simply given a correct extension and moved to a sensible directory, ex: <dest>/pdf/XYZ.pdf

# Installing dependencies
Create a new virturalenv and use:

	pip install -r requirements.txt

The filemagic library also requires libmagic to be installed on the system. Use homebrew or a similar utility to install "libmagic"

    brew install libmagic

## Generally good ideas for restoring from corrupted media

If you're attempting to recover data from known (or suspected to be) failing disk it's usually a good idea to make an image of the affected media, then work off that image. Use `dd if=/dev/my_sd_card of=/path/to/sd_backup.img'` to create the disk image, then use `mount -o loop,ro /path/to/sd_backup.img /mnt/sd_recovery` and work out of the /mnt/sd_recovery directory. Providing the "ro" option to mount means the image will be mounted read-only. The destination (-d arg) for recovered files then should of course be someplace other than inside of /mnt/sd_recovery
