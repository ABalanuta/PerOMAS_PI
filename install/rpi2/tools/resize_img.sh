
if [ $(id -u) -eq 0 ];
then # you are root, make the prompt red
	echo ""
else
    echo "Run as Root"
    exit
fi


if [ "$1" ]
then
	IMAGE_PATH=$(readlink -f "$1")
	echo "Using Image "$IMAGE_PATH
else
	echo "missing image file"
	exit
fi

if [[ `which rsync` ]]; then
        echo ""
else
        echo "Package 'rsync' is NOT installed."
        exit
fi

ORIGIN_ROOT_PATH="/tmp/origin/root/"
ORIGIN_BOOT_PATH="/tmp/origin/boot/"

TARGET_ROOT_PATH="/tmp/target/root/"
TARGET_BOOT_PATH="/tmp/target/boot/"

sudo mkdir -p $ORIGIN_ROOT_PATH
sudo mkdir -p $ORIGIN_BOOT_PATH
sudo mkdir -p $TARGET_ROOT_PATH
sudo mkdir -p $TARGET_BOOT_PATH

sudo losetup -D
SRC_LOOP_DEVICE=$(losetup -f)
sudo losetup -P $SRC_LOOP_DEVICE $IMAGE_PATH

LOOP_P1=$(sudo fdisk -l "$SRC_LOOP_DEVICE" | grep "/dev/loop" | grep p1 | awk '{print $1}')
LOOP_P2=$(sudo fdisk -l "$SRC_LOOP_DEVICE" | grep "/dev/loop" | grep p2 | awk '{print $1}')
#Mount Partitions
sudo mount $LOOP_P1 $ORIGIN_BOOT_PATH
sudo mount $LOOP_P2 $ORIGIN_ROOT_PATH


TARGET_IAMGE_PATH=$(dirname "$IMAGE_PATH")/$(basename "$IMAGE_PATH" .img)"_small.img"
ROOT_SIZE=$(sudo du -s /tmp/origin/root | awk '{print $1}')
BOOT_SIZE=$(sudo du -s /tmp/origin/boot | awk '{print $1}')
FREE_SIZE="576000"
TOTAL_SIZE=$(echo $BOOT_SIZE+$ROOT_SIZE+$FREE_SIZE | bc )

echo "Generating Empty target image of size: "$(echo $TOTAL_SIZE/1000 | bc )" MB"
sudo dd if=/dev/zero of=$TARGET_IAMGE_PATH bs=1024 count=$TOTAL_SIZE 2> /dev/null
DST_LOOP_DEVICE=$(losetup -f)
sudo losetup -P $DST_LOOP_DEVICE $TARGET_IAMGE_PATH

END_SIZE=$(sudo parted $DST_LOOP_DEVICE print | grep "Disk /dev" | awk '{print $3}')
sudo parted $DST_LOOP_DEVICE mklabel msdos 2> /dev/null
sudo parted $DST_LOOP_DEVICE mkpart primary fat16 1MiB 64MB 2> /dev/null
sudo parted $DST_LOOP_DEVICE mkpart primary ext4 64MB $END_SIZE 2> /dev/null

DST_P1=$DST_LOOP_DEVICE"p1"
DST_P2=$DST_LOOP_DEVICE"p2"

sudo mkfs.vfat $DST_P1 >/dev/null 2>&1
sudo mkfs.ext4 -j $DST_P2 >/dev/null 2>&1

sudo mount $DST_P1 $TARGET_BOOT_PATH
sudo mount $DST_P2 $TARGET_ROOT_PATH


sudo rsync -rltWDEgopt $ORIGIN_BOOT_PATH* $TARGET_BOOT_PATH --info=progress2 --no-inc-recursive
sudo rsync -rltWDEgopt $ORIGIN_ROOT_PATH* $TARGET_ROOT_PATH --info=progress2 --no-inc-recursive
sudo sync

echo "Modify files at: /tmp/target/"
read -p "Press [Enter] key to continue..."

echo "Unmounting"
sudo umount $ORIGIN_BOOT_PATH
sudo umount $ORIGIN_ROOT_PATH
sudo umount $TARGET_BOOT_PATH
sudo umount $TARGET_ROOT_PATH

sudo losetup -D
sudo chmod 777 $TARGET_IAMGE_PATH