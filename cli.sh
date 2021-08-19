#!/bin/bash

menu_text() {
    echo -e "\n\n***************************************"
    echo -e "********** POC - SPEED LAYER **********"
    echo -e "***************************************\n"
    echo -e "Options:"
    echo -e "\n1 - Setup Environment.\n"
    echo -e "2 - Start."
    echo -e "3 - Application Status."
    echo -e "4 - Tail Streaming. (WARNING: This will quit this client. To stop tailing press CTRL-C)."
    echo -e "5 - Open MongoDB Conteiner. (To quit the MongoDB container, press CTRL-D)."
    echo -e "6 - Remove all Containers."
    echo -e "7 - Remove all Persisted Data."
    echo -e "\n0 - Exit (Closes this client. No containers and/or data will be removed)."
}

show_menu() {
option="-1"
while [ $option != "0" ]
do
    clear
    menu_text

    echo -e "\nEnter an option:"
    read option

    if [ "$option" = "1" ]; then 
        setup
    elif [ "$option" = "2" ]; then
        start
    elif [ "$option" = "3" ]; then
        get_status
    elif [ "$option" = "4" ]; then
        tail_streaming
    elif [ "$option" = "5" ]; then
        open_mongo_container
    elif [ "$option" = "6" ]; then
        remove_containers
    elif [ "$option" = "7" ]; then
        remove_persisted
    elif [ "$option" = "0" ]; then
        exit
    else
        wrong_option
    fi
done
}

press_any_key() {
    echo -e "\nPress any key to continue..."
    read -n 1 -s
}

setup() {
    clear
    ./setup.sh
    press_any_key
}

start() {
    clear
    ./start.sh
    echo -e "\nAll containers have been started.\nPlease allow a couple of minutes until all services are running.\nEnjoy!"
    press_any_key
}

get_status() {
    clear
    sudo docker-compose ps
    press_any_key
}

tail_streaming() {
    clear
    ./tail-streaming.sh
}

open_mongo_container() {
    clear
    ./mongo.sh
}

remove_containers() {
    clear
    ./rm-containers.sh
    echo -e "\nAll containers have been removed."
    press_any_key
}

remove_persisted() {
    clear
    ./rm-persisted.sh
    echo -e "\nAll persisted data has been removed."
    press_any_key
}

exit() {
    clear
    echo -e "\nExiting the client.\nNote: No containers or persited data have been removed."
    press_any_key
}

wrong_option() {
    clear
    echo -e "\nWrong option. Please try again"
    press_any_key
}

show_menu