![My Backup Utilities](https://socialify.git.ci/taseikyo/backup-utils/image?forks=1&issues=1&language=1&owner=1&pattern=Brick%20Wall&pulls=1&stargazers=1&theme=Light "My Backup Utilities: a batch of useful code/scripts: run commands automatically, finish repetitive stupid operations, perform format conversions, etc.")

a batch of useful codes/scripts

*Afraid of accidental code loss, so I make this backup.*

## Bash

1. 001_get_process_pid_and_meminfo.sh: get pid according to process-name and print process memory info
2. 002_print_cpu_info.sh: print cpu information (l1 - l3 cache size/type)
3. 003_run_cmd_on_each_nodes.sh: run input command on each node (numa architecture)
4. 004_kill_process_via_name.sh: kill the process you input the name
1. 005_convert_pdf_to_eps.sh: Convert PDF to eps (encapsulated PostScript)

## JavaScript

1. 001_web-font-style-beautification.js: Set the web font to Microsoft Yahei (used in [tampermonkey](https://www.tampermonkey.net/))

## Python

1. ~001_qrc_to_lrc.py: convert qq lyric (.qrc) fromat to lrc~
2. 002_clear_netease_cloud_music_cache.py: clear netease-cloud-music cache
3. 003_convert_mp4_to_ts_and_merge.py: convert flv to mp4, convert mp4 to ts and then merge ts to mp4
4. 004_build_and_run_osv.py: build and run osv
5. 005_obtain_video_play_info.py: obtain video information that exceeds the play threshold
6. 006_auto_generate_toc.py: automatically generate a toc for markdown files
7. 007_complete_image_path_for_paper_notes.py: complete the path to images
8. 008_download_and_convert_b23_subtitle.py: download & convert bilibili cc subtitles to srt subtitle format
9. 009_file_time_infos.py: get file size, access time, modification time and creation time
10. 00A_video_resolution_duration.py: get video resolution and duration using `ffmpeg`
11. 00B_download_iqiyi_danmu_and_convert_b23_format.py: search and obtain iQiyi's danmu, and convert to Bilibili format
12. 00C_blogs_subscribe.py: pull subscribed blogs to local
13. ~00D_sublime-markdown-helper.py: A Sublime Text 3 plugin that can help write markdown faster (see .md doc for details)~，move to [sublime-markdown-helper](https://github.com/taseikyo/sublime-markdown-helper)
14. 00E_remove_duplicate_history_cmds.py: Remove duplicate commands in .zsh_history/.bash_history
15. 00F_pdf_cutter_tools.py: cut or merge pdfs!
16. 010_extract_images_from_qq_group_messages.py: Extract images from QQ group messages
1. 011_download_netease_music_lyric.py: Download lyrics from https://music.163.com
1. 012_zhihu_zhuanlan.py: Save the Zhihu column article as Markdown

## TypeScript

1. 001_medium_helper.ts: improve Medium.com reading experience (see [doc](TypeScript/001_medium_helper.md) for details)

## License

Copyright (c) 2019 Lewis Tian. Licensed under the MIT license.