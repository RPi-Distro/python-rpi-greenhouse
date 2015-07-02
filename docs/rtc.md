# Real Time Clock setup

- Enable `i2c` in `raspi-config`
- Add `dtoverlay=i2c-rtc,ds1307` to `/boot/config.txt`
- Check system date is correct, update if necessary
- Set RTC from system date with `sudo hwclock -w`
- Read RTC date with `sudo hwclock -r`
