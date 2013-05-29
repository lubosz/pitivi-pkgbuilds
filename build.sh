#/!bin/sh

#PACKAGES=`ls -d */`

PACKAGES="gstreamer-git
gst-plugins-base-git
gst-plugins-good-git
gst-plugins-bad-git
gst-plugins-ugly-git
gst-libav-git
gnonlin-git
gst-editing-services-git
pitivi-git"

if [ "$1" = "build" ]; then
  echo "foo"
fi

for PACKAGE in $PACKAGES; do
  echo "Building $PACKAGE"
  cd $PACKAGE
  makepkg -i
  cd ..
done;
