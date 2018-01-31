# How to reset camera:

## Save the following as `usbreset.c`


``` c
/* usbreset -- send a USB port reset to a USB device */


#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

#include <linux/usbdevice_fs.h>


int main(int argc, char **argv)
{
    const char *filename;
    int fd;
    int rc;

    if (argc != 2) {
        fprintf(stderr, "Usage: usbreset device-filename\n");
        return 1;
    }
    filename = argv[1];

    fd = open(filename, O_WRONLY);
    if (fd < 0) {
        perror("Error opening output file");
        return 1;
    }

    printf("Resetting USB device %s\n", filename);
    rc = ioctl(fd, USBDEVFS_RESET, 0);
    if (rc < 0) {
        perror("Error in ioctl");
        return 1;
    }
    printf("Reset successful\n");

    close(fd);
    return 0;
}

```

## Then run the following commands in terminal:

1. Compile the program:

	``` bash
	$ cc usbreset.c -o usbreset
	```

2. Get the Bus and Device ID of the USB device you want to reset:

	``` bash
	$ lsusb
	``` 

3. Make our compiled program executable:
	
	``` bash
	$ chmod +x usbreset
	```

4. Execute the program with sudo privilege; make necessary substitution for <Bus> and <Device> ids as found by running the lsusb command:

	``` bash
	$ sudo ./usbreset /dev/bus/usb/002/003
	```   

