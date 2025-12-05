#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

// returning non secure packet
const char *start_packet(void) {
    return "(SS,RFMP,v1.0,0)";
}

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Error creating socket");
        return 1;
    }

    struct sockaddr_in server_addr = {0};
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8082);  

    if (inet_pton(AF_INET, "127.0.0.1" , &server_addr.sin_addr) <= 0) {
        perror("Invalid IP address");
        close(sock);
        return 1;
    }

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        close(sock);
        return 1;
    }

    printf("Connected to server.\n");

    // sending the start packet
    const char *sp = start_packet();
    printf("Sending: %s\n", sp);
    if (send(sock, sp, strlen(sp), 0) < 0) {
        perror("send failed");
        close(sock);
        return 1;
    }

    // getting server response  
    char buffer[1024];
    int bytes = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (bytes > 0) {
        buffer[bytes] = '\0';
        printf("Server says: %s\n", buffer);
    } else {
        perror("Server closed connection early");
        close(sock);
        return 1;
    }

    // while loop-
    while (1) {
        char filename[256];
        printf("Please enter a File you want to read (or type exit to quit): ");
        if (!fgets(filename, sizeof(filename), stdin))
            break;

        // strip newline
        filename[strcspn(filename, "\n")] = '\0';

        // checks if exit was mentioned
        if (strcmp(filename, "exit") == 0)
            break;
        // if it was not mentioned we contiune
        if (strlen(filename) == 0)
            continue;

        char command_packet[300];
        snprintf(command_packet, sizeof(command_packet),
                 "(CM,openRead,%s)", filename);

        printf("Sending: %s\n", command_packet);
        if (send(sock, command_packet, strlen(command_packet), 0) < 0) {
            perror("send failed");
            break;
        }

        // receive server response
        bytes = recv(sock, buffer, sizeof(buffer) - 1, 0);
        if (bytes <= 0) {
            printf("Server disconnected.\n");
            break;
        }
        buffer[bytes] = '\0';
        printf("Server response: %s\n", buffer);
    }

    printf("Done\n");
    close(sock);
    return 0;
}