#!/usr/bin/env bash

die() {
    echo >&2 "$@"
    exit 1
}

checkStatus () {
    #echo "checkStatus method for $2 "
    command_status=$1
    if [ $command_status != "0" ]
    then
        echo " last command $2 not executed successfully :: exit the script"
        exit 0
    else
        echo " last command $2 executed successfully "
    fi
}

if [ "$#" -eq  2 ]
then
    echo "Arguments are validated"
else
    die "2 Arguments required, $# provided"
fi

echo "++++++++++++++++++++++++++++++++++++++++++++++"
echo "NFS install "
echo "++++++++++++++++++++++++++++++++++++++++++++++"
#$1 is name
#$2 is the file system
temp_dir="$PWD"/conf/pxe_cluster


if [ -f packages/images/"$2" ]
then
    echo "File system archive $2 exists."
else
    echo "Error: FS Archive $2  does not exists."
	exit 0
fi

if [ -d /nfs ]
then
    echo "NFS Mount point exists."
else
    echo "Creating NFS Mount point"
    sudo mkdir /nfs
    command_statustemp_dir="$PWD"/conf/pxe_cluster
=$?
	checkStatus $command_status " creating root NFS mount  "

fi

if [ -d /nfs/"$1" ]
then
    echo "NFS Mount point $1 already exists."
else
    echo "Creating NFS Mount point for $1"
    sudo mkdir /nfs/"$1"
    command_sttemp_diratus=$?
	checkStatus $command_status " creating NFS mount for $1  "

    #untar file system to NFS mount
    sudo tar --same-owner -xvf packages/images/"$2" -C /nfs/"$1"
    command_status=$?
	checkStatus $command_status " untaring file system for $1  "



    #add this directory to etc/exports
    echo "/nfs/$1/ *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
    command_status=$?
	checkStatus $command_status " adding $1 directory to exports  "

cat <<EOF >$temp_dir/hostname
$1
EOF

    sudo cp $temp_dir/hostname /nfs/$1/etc/hostname
    command_status=$?
	checkStatus $command_status " copying hostname  "

    #Start NFS and RPCBind services
    rpcstatus = sudo systemctl status rpcbind.service
    if [$rpcstatus == "Unit bob.service could not be found."]
    then
        sudo systemctl enable rpcbind.service
        sudo systemctl start rpcbind.service
        command_status=$?
	    checkStatus $command_status " starting rpcbind  "
    else
        sudo systemctl restart rpcbind.service
        command_status=$?
	    checkStatus $command_status " restarting rpcbind  "
    fi

    nfsstatus = sudo systemctl status nfs-kernel-server.service
    if [$rpcstatus == "Unit nfs-kernel-server.service could not be found."]
    then
        sudo systemctl enable nfs-kernel-server.service
        sudo systemctl start nfs-kernel-server.service
        command_status=$?
	    checkStatus $command_status " starting nfs-kernel-server  "
    else
        sudo systemctl restart nfs-kernel-server.service
        command_status=$?
	    checkStatus $command_status " restarting nfs-kernel-server  "
    fi

fi
