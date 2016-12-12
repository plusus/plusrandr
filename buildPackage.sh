#!/bin/bash -e

PACKAGE_NAME=plusrandr
VERSION_MAJOR=1
VERSION_MINOR=0
VERSION_BUILD=2
VERSION="$VERSION_MAJOR.$VERSION_MINOR-$VERSION_BUILD"
SEP="_"
PACKAGE_NAME_VERSION=$PACKAGE_NAME$SEP$VERSION
ARCHITECTURE=all
PACKAGE_DIR=builddeb/$PACKAGE_NAME_VERSION

echo '### COPYING FILES'
rm -rf $PACKAGE_DIR/*
INSTALL_DIR=$PACKAGE_DIR/usr/lib/python2.7/dist-packages
mkdir -p $INSTALL_DIR
cp -r plusrandr $INSTALL_DIR/

# Icon
mkdir -p $PACKAGE_DIR/usr/share/icons/hicolor/scalable/apps
cp plusrandr/res/plusrandr_icon.svg $PACKAGE_DIR/usr/share/icons/hicolor/scalable/apps/plusrandr.svg

# Desktop file
mkdir -p $PACKAGE_DIR/usr/share/applications
cp desktop/plusrandr.desktop $PACKAGE_DIR/usr/share/applications/

echo '### CREATING DEBIAN FOLDER'
mkdir -p $PACKAGE_DIR/DEBIAN
# Copy base files
rsync -a debian/ $PACKAGE_DIR/DEBIAN/

mkdir -p $PACKAGE_DIR/usr/bin
ln -s /usr/lib/python2.7/dist-packages/plusrandr/plusrandr_gui.py $PACKAGE_DIR/usr/bin/plusrandr

cd builddeb/$PACKAGE_NAME_VERSION

# Generate control file
CONTROL_FILE="DEBIAN/control"
touch DEBIAN/control
echo "Package: ${PACKAGE_NAME}" > "$CONTROL_FILE"
echo "Version: $VERSION" >> "$CONTROL_FILE"
echo "Section: misc" >> "$CONTROL_FILE"
echo "Priority: optional" >> "$CONTROL_FILE"
echo "Architecture: $ARCHITECTURE" >> "$CONTROL_FILE"
echo "Essential: no" >> "$CONTROL_FILE"
echo "Installed-Size: `du -sc usr | grep total | awk '{ print $1 }'`" >> "$CONTROL_FILE"
echo "Maintainer: Antoine Girard-Vallee <antoine.girard-vallee@usherbrooke.ca>" >> "$CONTROL_FILE"
echo "Homepage: http://plus-us.gel.usherbrooke.ca/plusrandr" >> "$CONTROL_FILE"
echo "Depends: python (>= 2.7), python-pyside (>= 1.2), x11-xserver-utils" >> "$CONTROL_FILE"
echo "Description: High-level frontend to multi-monitor handling" >> "$CONTROL_FILE"
echo " High-level frontend to xrandr that allows to easily switch between monitors and mirror them efficently." >> "$CONTROL_FILE"

# Create md5sum
find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '"%P" ' | xargs md5sum > DEBIAN/md5sums

cd ..

dpkg-deb -bv $PACKAGE_NAME_VERSION $PACKAGE_NAME_VERSION"_"$ARCHITECTURE".deb"
