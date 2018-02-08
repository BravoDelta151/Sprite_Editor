# Sprite_Editor

To run (requires python 3)
>python main.py


See help.jpg for instructions...

All buttons work!
Brush or Fill: fill one pixel at a time with brush or fill a range

Load: Loads an existing bank from the banks folder.  Enter the name without the .bmp extension.  All banks are bmps
New: reset to a blank strip (bank)
Save, Save As: save the bank (strip) to the banks folder.  Enter the name with the .bmp extension.  Save As will not let you overwrite a file.  Save overwrites.  This will be changed in the future.

Update: *** This updates changes made in the pixels to the bank (strips to the right of the buttons).  If you change frames without updating, changes will be lost (I am working on an auto-update). 

## TODO:
- merge palette from image 

the palettes can be defined in the data folder but the filename is currently hard-coded.  
The default is an NES palette from http://www.thealmightyguru.com/Games/Hacking/Wiki/index.php/NES_Palette