#!/bin/bash

# https://qiita.com/ksksue@github/items/023f7675faec5d367956

vcgencmd get_throttled # throttled=0x0 is fine
vcgencmd measure_temp # now 65.9'C
vcgencmd measure_clock arm # frequency(48)=600000000
vcgencmd measure_volts # volt=1.2000V
vcgencmd get_mem arm # arm=948M
vcgencmd get_mem gpu # gpu=76M
vcgencmd get_config int
# aphy_params_current=819
# arm_freq=900
# arm_freq_min=600
# audio_pwm_mode=514
# camera_auto_detect=1
# config_hdmi_boost=5
# disable_auto_turbo=1
# disable_commandline_tags=2
# disable_l2cache=1
# disable_overscan=1
# display_auto_detect=1
# display_hdmi_rotate=-1
# display_lcd_rotate=-1
# dphy_params_current=547
# dvfs=3
# enable_tvout=1
# enable_uart=1
# force_eeprom_read=1
# force_pwm_open=1
# framebuffer_ignore_alpha=1
# framebuffer_swap=1
# init_uart_clock=0x2dc6c00
# lcd_framerate=60
# mask_gpu_interrupt0=3072
# mask_gpu_interrupt1=26370
# max_framebuffers=2
# over_voltage_avs=0x1b774
# pause_burst_frames=1
# program_serial_random=1
# sdram_freq=450
# total_mem=1024
# hdmi_force_cec_address:0=65535
# hdmi_force_cec_address:1=65535
# hdmi_pixel_freq_limit:0=0x9a7ec80
