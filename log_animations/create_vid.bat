REM ffmpeg -framerate 24 -i mult_1600.log/%%04d.png output.mp4
ffmpeg -y -framerate 24 -i best.log/%%06d.png output.mp4
ffmpeg -y -i output.mp4 -filter_complex "[0]trim=0:2[a];[0]setpts=PTS-2/TB[b];[0][b]overlay[c];[a][c]concat" final_output.mp4
