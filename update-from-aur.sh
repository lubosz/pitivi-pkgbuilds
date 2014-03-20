PACKAGES="gst-devtools-git
gst-libav-git
gst-plugins-base-git
gst-plugins-good-git
gstreamer-git
gnonlin-git
gst-editing-services-git
gst-plugins-bad-git
gst-plugins-gl-git
gst-plugins-ugly-git
pitivi-git"

mkdir old

for PACKAGE in $PACKAGES; do
  echo "Updating $PACKAGE"
  #cd $PACKAGE
  mv $PACKAGE old/$PACKAGE
  packer -G $PACKAGE
  #if [ "$2" = "rebuild" ]; then
  #  makepkg -if
  #else
  #  makepkg -i
  #fi
  #cd ..
done;
rm *.tar.gz
