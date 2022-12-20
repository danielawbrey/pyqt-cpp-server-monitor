#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <regex>
#include <sstream>
#include <vector>
#include <unistd.h>
#include "helper.h"

using namespace std;

void sendMessage(int serverSocket, const char* replyMessage, struct sockaddr_in client, socklen_t length) {
    int reply = sendto(serverSocket, replyMessage, strlen(replyMessage), 0, (struct sockaddr *) &client, length);
    if(reply < 0)
        cout << "Sending error" << endl;
}

char* getMessageRespose(int serverSocket, char* buffer, struct sockaddr_in client, socklen_t length) {
    // Receive test description message
    int receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length);
    if(receivedMessage < 0)
        cout << "Reply error" << endl;

    return buffer;
}

int main(int argc, char *argv[]) {
    const char* ip_address = "127.0.0.1", flag = 1;
    const char* replyMessage = "123;MODEL=3454;SERIAL=25356;";
    int port = atoi(argv[1]), receivedMessage = 0, udp_descriptor, listen_descriptor;
    int serverSocket = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in server, client;
    socklen_t addressSize = sizeof(client), length = sizeof(server);
    char buffer[64];
    vector<string> testDescriptionParts;
    string s = "";

    memset(&server, '\0', sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(ip_address);

    if(bind(serverSocket, (struct sockaddr*)&server, sizeof(server)) < 0)
        cout << "Binding error" << endl;

    while(true) {
        cout << "Waiting for discovery message" << endl;

        // Listen for discovery message
        receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length);
        if(receivedMessage < 0)
            cout << "Reply error" << endl;

        // If pattern matches discovery message
        if(regex_match(buffer, regex("[0-9]+;"))) {
            cout << "Dicovery message received from device: " << buffer << endl;

            bzero(buffer, sizeof(buffer));

            sendMessage(serverSocket, "123;MODEL=3454;SERIAL=25356;", client, length);

            sendMessage(serverSocket, "TEST;RESULT=STARTED;", client, length);

            // Receive test description message
            receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length);
            if(receivedMessage < 0)
                cout << "Reply error" << endl;

            cout << "Test description " << buffer << endl;

            testDescriptionParts = getDescriptionParts(splitString(convertArrayToString(buffer, 64)));

            bzero(buffer, sizeof(buffer));

            while (true) {
                // Listen for stop message from client
                
                s = to_string(rand() % 10) + ";" + to_string(rand() % 10);
                replyMessage = s.c_str();
                sendMessage(serverSocket, replyMessage, client, length);
                
                receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length);
                if(receivedMessage < 0)
                    cout << "Reply error" << endl;
                
                if(strcmp(buffer, "TEST;CMD=STOP;") == 0) {
                    cout << "Stop command received" << endl;

                    response = sendMessage(serverSocket, "TEST;RESULT=STOPPED;", client, length);
                                        
                    bzero(buffer, sizeof(buffer));

                    break;
                }

                bzero(buffer, sizeof(buffer));

                usleep(stoi(testDescriptionParts[1]));
            }
        }

        bzero(buffer, sizeof(buffer));

    }

    return 0;
}