#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
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
    int receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length);
    if(receivedMessage < 0)
        cout << "Reply error" << endl;
    
    return buffer;
}

void initializeSocket(struct sockaddr_in server, const char* ipAddress, int port) {
    memset(&server, '\0', sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(ipAddress);

    if(bind(serverSocket, (struct sockaddr*)&server, sizeof(server)) < 0)
        cout << "Binding error" << endl;
}

int main(int argc, char *argv[]) {
    const char* replyMessage = "123;MODEL=3454;SERIAL=25356;";
    const int bufferSize = 64;
    char buffer[bufferSize];
    int receivedMessage = 0, serverSocket = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in server, client;
    socklen_t addressSize = sizeof(client), length = sizeof(server);  
    vector<string> testDescriptionParts;
    
    initializeSocket(server, "127.0.0.1", atoi(argv[1]));

    while(true) {
        cout << "Waiting for discovery message..." << endl;

        receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length); // Listen for discovery message
        if(receivedMessage < 0)
            cout << "Reply error" << endl;

        if(regex_match(buffer, regex("[0-9]+;"))) { // Match discovery message pattern
            cout << "Dicovery message received from device: " << buffer << endl;

            bzero(buffer, sizeof(buffer));

            sendMessage(serverSocket, "123;MODEL=3454;SERIAL=25356;", client, length);

            sendMessage(serverSocket, "TEST;RESULT=STARTED;", client, length);

            receivedMessage = recvfrom(serverSocket, buffer, sizeof(buffer), 0, (struct sockaddr*) &client, &length); // Receive test description message
            if(receivedMessage < 0)
                cout << "Reply error" << endl;

            cout << "Test description " << buffer << endl;

            testDescriptionParts = getDescriptionParts(splitString(convertArrayToString(buffer, bufferSize)));

            bzero(buffer, sizeof(buffer));
        }

        bzero(buffer, sizeof(buffer));

    }

    return 0;
}