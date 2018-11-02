# -*- Coding: UTF-8 -*-
# coding: utf-8
import watch_directory

for file_type, filename, action in watch_directory.watch_path ("C:/xampp/htdocs/PATH/source_codes"):
    print file_type, filename, action


    