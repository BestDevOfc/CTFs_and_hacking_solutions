// clang -dynamiclib -o hack.dylib hack.c -framework CoreFoundation -framework Foundation -lpthread
// DYLD_INSERT_LIBRARIES=./hack.dylib ./main


// hook.cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <mach-o/dyld.h>
#include <dlfcn.h>
#include <string.h>
#include <pthread.h>

// Define the offset from the data segment base to the 'money' variable


// Function to get the base address of the main executable
void* getBaseAddress() {
    uint32_t count = _dyld_image_count();
    for (uint32_t i = 0; i < count; i++) {
        const char *name = _dyld_get_image_name(i);
        if( name && strstr( name, "/main" ) != NULL ){
            void *base = (void *)_dyld_get_image_header(i);
            if (base) {
                printf("[ DYLD Image Name %s (%p)]\n", name, base);
                return base;
            }
        }
    }
    return NULL;
}

void* get_data_segment_from_base_address( void* base_address ){
    need to get the base address o the __DATA section of the main base address ( I know sounds confusing ),
    this is because cheat engine's pointer to the money variable is this: "dyld.DATA"+000002A0
}

void* hack_thread(){
    void* base_address = getBaseAddress();
    // Get the base address of the main executable

    if( base_address == NULL ){
        fprintf( stderr, "[ Failed to get base address! ]\n" );
    }
    return NULL;
}


// Constructor function that runs when the DYLIB is loaded
__attribute__((constructor))
void init() {
    printf("DYLIB Injected!\n");
    
    pthread_t thread_ID;

    int thread_creation_status = pthread_create( &thread_ID, NULL, hack_thread, NULL );
    if( thread_creation_status != 0 ){
        fprintf(stderr, "[ Failed to create the hack_thread ! ]\n");
    }

    // Detach so the thread runs independently without waiting for it
    pthread_detach(thread_ID); 
}
