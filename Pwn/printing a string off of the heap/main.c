// flagfest CTF 2024
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void displayStatus();
void engageHyperdrive();
void fireWeapons();
void activateShields();
void scanForEnemies();
void performMaintenance();

#define MAX_USERNAME_LENGTH 16
#define MAX_PASSWORD_LENGTH 16
#define MAX_API_KEY_LENGTH 256

char* readApiKeyFromFile(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return NULL;
    }

    /*
    NOTE: the flag is stored in the heap
    
    */
    char *apiKey = malloc(MAX_API_KEY_LENGTH * sizeof(char));
    if (apiKey == NULL) {
        perror("Memory allocation failed");
        fclose(file);
        return NULL;
    }

    if (fgets(apiKey, MAX_API_KEY_LENGTH, file) != NULL) {
        size_t len = strlen(apiKey);
        if (len > 0 && apiKey[len - 1] == '\n') {
            apiKey[len - 1] = '\0';
        }
    } else {
        perror("Error reading API key");
        free(apiKey);
        apiKey = NULL;
    }

    fclose(file);
    return apiKey;
}

int console(char username[]){
    char choice;
    char user[MAX_USERNAME_LENGTH];
    strncpy(user,username,MAX_USERNAME_LENGTH);

    printf("\e[1;1H\e[2J");

    do {
        printf("\n--- Imperial Star Destroyer Main Console ---\n");
        printf("Current User: ");
        printf("\033[0;35m");
        printf(user);
        printf("\033[0m\n");
        printf("1. Display Ship Status\n");
        printf("2. Engage Hyperdrive\n");
        printf("3. Fire Weapons\n");
        printf("4. Activate Shields\n");
        printf("5. Scan for Enemies\n");
        printf("6. Perform Maintenance\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        scanf("%s", &choice);
        /*
        NOTE: buffer overflow, can write into the username using format specifiers

        
        
        */

        printf("\e[1;1H\e[2J");

        switch(choice) {
            case '1':
                displayStatus();
                break;
            case '2':
                engageHyperdrive();
                break;
            case '3':
                fireWeapons();
                break;
            case '4':
                activateShields();
                break;
            case '5':
                scanForEnemies();
                break;
            case '6':
                performMaintenance();
                break;
            case '0':
                printf("\033[0;31mExiting spaceship console...\033[0m\n");
                break;
            default:
                printf("\033[0;31mInvalid choice. Please try again.\033[0m\n");
        }
    } while(choice != '0');
}

int validateUsername(char *username) {
    for (int i = 0; i < strlen(username); i++) {
        if (username[i] == '%') {
            return 0;
        }
    }
    return 1;
}

int main() {
    const char *filename = "flag.txt";
    char *apiKey = readApiKeyFromFile(filename);
    /*
    
    NOTE: the address pointing to the string in HEAP is stored on the STACK, 
    we can use %s to dereference it and print that string with format specifier 
    vulnerability.

    A%18$s
    ^^ still works even with PIE bcs we can use offsets still just the base binary 
        address will be randomized every runtime.
    
    */

    char username[MAX_USERNAME_LENGTH];
    char password[MAX_PASSWORD_LENGTH];
    const char correctPassword[] = getenv("password"); //BUGFIX: Hardcoded Credentials Leftover in v1

    printf("Imperial Star Destroyer Main Console v2\n");
    printf("\033[1;31mWARNING: ONLY AUTHORIZED OFFICERS SHOULD ACCESS THIS CONSOLE\033[0m\n\n");

    do {
        printf("Enter username: ");
        scanf("%15s", username);

        if (validateUsername(username))
            break;

        printf("\033[0;31mInvalid username. Username cannot contain '%%'.\033[0m\n");
    } while (1);

    printf("Enter password: ");
    scanf("%15s", password);

    if (strcmp(password, correctPassword) != 0) {
        printf("\033[0;31mIncorrect password.\033[0m\n");
        return 1;
    }


    console(username);
}

void displayStatus() {
    printf("\n--- Ship Status ---\n");
    printf("Hull Integrity: \033[0;32m95%%\033[0m\n");
    printf("Shields: \033[0;33m80%%\033[0m\n");
    printf("Weapon Systems: \033[0;32mOnline\033[0m\n");
    printf("Hyperdrive: \033[0;32mReady\033[0m\n");
}

void engageHyperdrive() {
    printf("\nEngaging hyperdrive... Stand by!\n");
    printf("Hyperdrive activated. Destination:\033[0;36m Tatooine\033[0m\n");
}

void fireWeapons() {
    printf("\nFiring all weapons!\n");
    printf("\033[0;32mLasers and torpedoes fired.\033[0m\n");
}

void activateShields() {
    printf("\nActivating shields...\n");
    printf("\033[0;32mShields at maximum power.\033[0m\n");
}

void scanForEnemies() {
    printf("\nScanning for enemies...\n");
    printf("\033[0;32mNo enemy ships detected within range.\033[0m\n");
}

void performMaintenance() {
    printf("\nPerforming routine maintenance...\n");
    printf("\033[0;32mAll systems operating within normal parameters.\033[0m\n");
}