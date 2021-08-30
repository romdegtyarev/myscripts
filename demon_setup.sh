#!/bin/bash

SCRIPT=$1
SERVICE_NAME=$2
SERVICE_DESCR=$3

initd_install() {
    cp $SCRIPT /etc/init.d/
    cd /etc/rc2.d
    ln -s ../init.d/$SCRIPT ./S99$SCRIPT
}

initd_uninstall() {
    rm -rf /etc/rc0.d/K10$SCRIPT
    rm -rf /etc/rc6.d/K10$SCRIPT
    rm -rf /etc/rc2.d/S99$SCRIPT
    rm -rf /etc/init.d/$SCRIPT
}

SYSTEMD_EXEC_PATH=/usr/local/bin
SERVICE_PATH=/usr/local/lib/systemd/system
SERVICE_NAME=$SERVICE_NAME.service
SYSTEMD_SERVICE=$SERVICE_PATH/$SERVICE_NAME

systemd_install() {
    cp $SCRIPT $SYSTEMD_EXEC_PATH

    mkdir -p $SERVICE_PATH

    echo "[Unit]" > $SYSTEMD_SERVICE
    echo "Description=$SERVICE_DESCR" >> $SYSTEMD_SERVICE
    echo "StopWhenUnneeded=true" >> $SYSTEMD_SERVICE

    echo "[Service]" >> $SYSTEMD_SERVICE
    echo "Type=oneshot" >> $SYSTEMD_SERVICE
    echo "ExecStart=$SYSTEMD_EXEC_PATH/$SCRIPT" >> $SYSTEMD_SERVICE
    echo "RemainAfterExit=yes" >> $SYSTEMD_SERVICE

    echo "[Install]" >> $SYSTEMD_SERVICE
    echo "WantedBy=multi-user.target" >> $SYSTEMD_SERVICE

    chmod 0644 $SYSTEMD_SERVICE;
    systemctl enable $SERVICE_NAME.service;
}

systemd_uninstall() {
    rm $SYSTEMD_EXEC_PATH/$SCRIPT
    systemctl disable $SERVICE_NAME.service;
    rm $SYSTEMD_SERVICE
}

if [[ !( $USER = root ) ]]; then
    echo "Permision denied, run as root";
    exit 0;
fi

if [[ $# -ne 3 ]]; then
    echo "Use: $0 /path_to_/script.sh service_name service_description"
    exit -1
fi

echo "What you want do?";
echo "1. Install demon";
echo "2. Uninstall demon";
echo;
echo -n "Input: ";

read val;

if [[ $val == "1" ]]; then
    echo "What boot system you have?";
    echo "1. Init.d";
    echo "2. System.d";
    read val;
    if [[ $val == "1" ]]; then
        initd_uninstall;
        initd_install;
    elif [[ $val == "2" ]]; then
        systemd_uninstall;
        systemd_install;
    else
        echo "Wrong point menu";
        exit -1;
    fi
    echo "Demon successful install";
elif [[ $val == "2" ]]; then
    echo "What boot system you have?";
    echo "1. Init.d";
    echo "2. System.d";
    read val;
    if [[ $val == "1" ]]; then
        initd_uninstall;
    elif [[ $val == "2" ]]; then
        systemd_uninstall;
    else
        echo "Wrong point menu";
        exit -1;
    fi
    echo "Demon successful uninstall";
else
    echo "Wrong point menu";
fi


