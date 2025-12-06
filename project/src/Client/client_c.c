#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

// Construct SS packet
const char *start_packet(void) {
    return "(SS,RFMP,v1.0,0)";
}

// Construct End packet
const char *end_packet(void) {
    return "(End)";
}

int main() {
//Sock_Stream = TCP
    int sock = socket(AF_INET, SOCK_STREAM, 0);
// Checks if socket created
    if (sock < 0) {
        perror("Error creating socket");
        return 1;
    }
// Structure with server IP and port number
    struct sockaddr_in server_addr = {0};
// AF_INET = Use IPv4
    server_addr.sin_family = AF_INET;
//server port = 8082
    server_addr.sin_port = htons(8082);

//specify server address
    inet_pton(AF_INET, "127.0.0.1" , &server_addr.sin_addr);
//connect to server
    connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
    printf("Connected to server...\n");

// send the start packet
    const char *sp = start_packet();
    printf("Sending: %s\n", sp);
    if (send(sock, sp, strlen(sp), 0) < 0) {
        perror("send failed");
        close(sock);
        return 1;
    }

// get server response so SC and DP  
    char buffer[1024];
    int bytes = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (bytes > 0) {
        buffer[bytes] = '\0';
        printf("Server response... %s\n", buffer);
    }

    while (1) {
        char filename[256];
        printf("File to read or exit to leave: ");
	
	//get user input and handle errors
        if (fgets(filename, sizeof(filename), stdin) == NULL) {
            printf("Error file not specified\n");
            break;
        }

        // strips enter key \n from the user input 
        filename[strcspn(filename, "\n")] = '\0';

        // checks if exit was mentioned and send end_packet
        if (strcmp(filename, "exit") == 0) {
            const char *ep = end_packet();
            printf("Sending (End) packet to server... %s\n", ep);
            send(sock, ep, strlen(ep), 0);
            close(sock);
            break;
        }

        // if user input is empty then redo
        if (strlen(filename) == 0)
            continue;
	
        char command_packet[300];
	//Build CM packet for openRead and save it to command_packet
        snprintf(command_packet, sizeof(command_packet), "(CM,openRead,%s)", filename);

        printf("Sending: %s\n", command_packet);
        send(sock, command_packet, strlen(command_packet), 0);

        // receive server response
        bytes = recv(sock, buffer, sizeof(buffer) - 1, 0);


	//handle no server answer
        if (bytes <= 0) {
            perror("Error coundnt recive the packet from server");
            close(sock);
            break;
        }
	//format and print server answer
        buffer[bytes] = '\0';
        printf("Server response... %s\n", buffer);
    }

    return 0;
}