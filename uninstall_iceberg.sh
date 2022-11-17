#!/bin/sh

## REMINDER: YOU NEED TO RUN THIS SCRIPT VIA SUDO

#################################################
##    KILL THE EXECUTION OF THE EXECUTABLES    ##
#################################################

/bin/ps -axcopid,command | /usr/bin/grep "Iceberg*" | /usr/bin/awk '{ system("kill -9 "$1) }'

if [ -f /Library/LaunchDaemons/fr.whitebox.iceberg.plist ]; then

    sudo launchctl unload /Library/LaunchDaemons/fr.whitebox.iceberg.plist

else

    /bin/ps -axcopid,command | /usr/bin/grep "IcebergControlTowerTool*" | /usr/bin/awk '{ system("kill -9 "$1) }'

fi

/bin/ps -axcopid,command | /usr/bin/grep "IcebergBuilder*" | /usr/bin/awk '{ system("kill -9 "$1) }'

#################################################
##         REMOVE THE FILES FROM DISK          ##
#################################################

## APPLICATION

if [ -d /Applications/Iceberg.app ]; then
   /bin/rm -r /Applications/Iceberg.app
fi

## APPLICATION SUPPORT

if [ -d /Library/Application\ Support/Iceberg ]; then
   /bin/rm -r /Library/Application\ Support/Iceberg
fi

## FRAMEWORKS

## We don't remove the MOKit Framework because it can be used by other applications.

## STARTUPITEM

if [ -d /Library/StartupItems/IcebergControlTower ]; then
   /bin/rm -r /Library/StartupItems/IcebergControlTower
fi

if [ -f /Library/LaunchDaemons/fr.whitebox.iceberg.plist ]; then

   /bin/rm -r /Library/LaunchDaemons/fr.whitebox.iceberg.plist
   
fi

## BINARY TOOL

## Old location

if [ -f /usr/bin/freeze ]; then
   /bin/rm /usr/bin/freeze
fi

if [ -f /usr/local/bin/freeze ]; then
   /bin/rm /usr/local/bin/freeze
fi

if [ -f /usr/local/bin/goldin ]; then
   /bin/rm /usr/local/bin/goldin
fi

## RECEIPTS

if [ -d /Library/Receipts/Iceberg.pkg ]; then
	/bin/rm -r /Library/Receipts/Iceberg.pkg
fi

exit 0