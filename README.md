# Proton Mail Export Sorter

Neccessary tool, due to legacy Import/Export app being discontinued, and replaced by Proton Mail Export Tool (https://proton.me/support/proton-mail-export-tool). For free users that is the only way to export entire mailbox, unfortunately it has its downsides. This replacment tool exports all emails (individual .eml files) into a single folder irrespective of their folders. It then attaches metadata .json files to each .eml file. These metadata files contain information about the folders the email is supposed to be in.

As email export and local archivation is a way of freeing up the email storage space without losing the emails, it is neccessary to make the export tool useful by sorting the emails into their corresponding folders. That is why the Proton Mail Export Sorter works, it sorts these files into directories for easy import into a email client of your choice, or just for archival purposes.

This script uses just built-in python libraries, and was tested on Python 3.13.2, but most likely it will work on older Python 3 versions as well. Just run the script in your python interpreter and provide the full path to your exported mailbox directory (the one containing all the .eml files).

If you have ideas on how to make it better, or any desired functionality, just write an issue! 🤝
