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
pitivi-git
wayland-git
glib2-git
gtk3-git
totem-git"

for PACKAGE in $PACKAGES; do
  echo "Building $PACKAGE"
  cd $PACKAGE
  
  if [ "$1" = "rebuild" ]; then
    makepkg -if
  else
    makepkg -i
  fi
  cd ..
done;
