#/!bin/sh

#PACKAGES=`ls -d */`

PITIVIPACKAGES="gstreamer-git
gst-plugins-base-git
gst-plugins-good-git
gst-plugins-bad-git
gst-plugins-ugly-git
gst-plugins-gl-git
gst-libav-git
gnonlin-git
gst-editing-services-git
pitivi-git"

TOTEMPACKAGES="wayland-git
glib2-git
libxi-git
gtk3-git
clutter-git
clutter-gst
cogl-git
totem-git"

WAYLANDPACKAGES="mesa-git
wayland-git
weston-git
glib2-git
gtk3-git"

if [ "$1" = "totem" ]; then
  PACKAGES=$TOTEMPACKAGES
else
  PACKAGES=$PITIVIPACKAGES
fi

for PACKAGE in $PACKAGES; do
  echo "Building $PACKAGE"
  cd $PACKAGE
  
  if [ "$2" = "rebuild" ]; then
    makepkg -if
  else
    makepkg -i
  fi
  cd ..
done;
