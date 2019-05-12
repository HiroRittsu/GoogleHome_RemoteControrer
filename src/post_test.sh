#!/bin/sh

curl -w '\n' 'http://cloud.ai-j.jp/manage/tunningpi/text-to-speech.php' --data 'text=%E3%83%86%E3%82%B9%E3%83%88&params%5Binput_type%5D=&params%5Bspeaker_name%5D=nozomi&params%5Bvolume%5D=1&params%5Bspeed%5D=1&params%5Bpitch%5D=1&params%5Brange%5D=1&params%5Bjoy%5D=0&params%5Bsadness%5D=0&params%5Banger%5D=0&params%5Bext%5D=mp3&params%5Bplaying_ext%5D=mp3&params%5Bcompany_id%5D=28&params%5Bservice_id%5D=1&params%5Buse_wdic%5D=0' -XPOST
